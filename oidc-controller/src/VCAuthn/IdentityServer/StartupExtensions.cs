using System.Linq;
using System.Reflection;
using IdentityServer4.EntityFramework.DbContexts;
using IdentityServer4.EntityFramework.Mappers;
using IdentityServer4.Validation;
using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using VCAuthn.IdentityServer.Endpoints;
using VCAuthn.Services.Contracts;
using VCAuthn.Services;
using VCAuthn.UrlShortener;
using VCAuthn.Utils;
using VCAuthn.IdentityServer.Endpoints.AuthorizeCallbackEndpoint;
using VCAuthn.Migrations;

namespace VCAuthn.IdentityServer
{
    public static class StartupExtensions
    {
        public static void AddAuthServer(this IServiceCollection services, IConfiguration config)
        {
            // Fetch the migration assembly
            var migrationsAssembly = typeof(StartupExtensions).GetTypeInfo().Assembly.GetName().Name;

            // Get connection string for database
            var connectionString = config.GetConnectionString("Database");

            // Register identity server
            services.AddIdentityServer(options =>
                {
                    options.Events.RaiseErrorEvents = true;
                    options.Events.RaiseInformationEvents = true;
                    options.Events.RaiseFailureEvents = true;
                    options.Events.RaiseSuccessEvents = true;
                    
                    // TODO: disable default endpoints that are not being used/available
                })
                .AddConfigurationStore(options =>
                {
                    options.ConfigureDbContext = b =>
                        b.UseNpgsql(connectionString, sql => sql.MigrationsAssembly(migrationsAssembly));
                })
                .AddOperationalStore(options =>
                {
                    options.ConfigureDbContext = b =>
                        b.UseNpgsql(connectionString, sql => sql.MigrationsAssembly(migrationsAssembly));
                    // this enables automatic token cleanup. this is optional.
                    options.EnableTokenCleanup = true;
                })

                .AddDeveloperSigningCredential( persistKey: false )

                // Custom Endpoints
                .AddEndpoint<AuthorizeEndpoint>(AuthorizeEndpoint.Name, IdentityConstants.VerifiedCredentialAuthorizeUri.EnsureLeadingSlash())
                .AddEndpoint<TokenEndpoint>(TokenEndpoint.Name, IdentityConstants.VerifiedCredentialTokenUri.EnsureLeadingSlash())
                .AddEndpoint<AuthorizeCallbackEndpoint>(AuthorizeCallbackEndpoint.Name, IdentityConstants.AuthorizeCallbackUri.EnsureLeadingSlash());

            services.AddScoped<IPresentationConfigurationService, PresentationConfigurationService>();
            services.AddScoped<ITokenIssuerService, TokenIssuerService>();

            services.AddTransient<ISecretParser, QueryStringSecretParser>();
        }

        public static void UseAuthServer(this IApplicationBuilder app, IConfiguration config)
        {
            InitializeDatabase(app, config);
            
            app.UseForwardedHeaders()
               .UseHttpsRedirection()
               .UseCors()
               .UseStaticFiles()
               .UseRouting()
               .UseIdentityServer();
        }

        public static void InitializeDatabase(IApplicationBuilder app, IConfiguration config)
        {
            var _logger = app.ApplicationServices.GetService<ILogger<Startup>>();

            // Init Identity server db
            using (var serviceScope = app.ApplicationServices.GetService<IServiceScopeFactory>().CreateScope())
            {
                // Resolve the required services
                var configContext = serviceScope.ServiceProvider.GetRequiredService<ConfigurationDbContext>();
                serviceScope.ServiceProvider.GetRequiredService<PersistedGrantDbContext>().Database.Migrate();

                // Migrate any required db contexts
                configContext.Database.Migrate();

                var currentIdentityResources = configContext.IdentityResources.ToList();
                foreach (var resource in Config.GetIdentityResources())
                {
                    if (currentIdentityResources.All(_ => resource.Name != _.Name))
                    {
                        configContext.IdentityResources.Add(resource.ToEntity());
                    }
                }
                configContext.SaveChanges();

                // Seed pre-configured clients
                var currentClients = configContext.Clients.ToList();

                foreach (var client in currentClients)
                {
                    _logger.LogDebug($"Existing client: [{client.ClientId} ; {client.Id}]");
                }

                var clients = Config.GetClients(config.GetSection("Clients"));
                foreach (var client in clients)
                {
                    var existingClient = currentClients.FirstOrDefault(_ => _.ClientId == client.ClientId);
                    if (existingClient != null)
                    {
                        _logger.LogDebug($"Updating client [{client.ClientId}]");
                        var c = client.ToEntity();
                        c.Id = existingClient.Id;
                        configContext.Entry(existingClient).CurrentValues.SetValues(c);
                    }
                    else
                    {
                        _logger.LogDebug($"Inserting client [{client.ClientId}]");
                        configContext.Clients.Add(client.ToEntity());
                    }
                    configContext.SaveChanges();
                }
                configContext.SaveChanges();
            }

            // Storage Db init
            using (var serviceScope = app.ApplicationServices.GetService<IServiceScopeFactory>().CreateScope())
            {
                var context = serviceScope.ServiceProvider.GetService<StorageDbContext>();
                context.Database.Migrate();
            }
        }

        public static void AddUrlShortenerService(this IServiceCollection services, IConfiguration config)
        {
            // Fetch the migration assembly
            var migrationsAssembly = typeof(StartupExtensions).GetTypeInfo().Assembly.GetName().Name;

            // Register the DB context
            services.AddDbContext<StorageDbContext>(options =>
                options.UseNpgsql(config.GetConnectionString("Database"), x => x.MigrationsAssembly(migrationsAssembly)));

            // Adds the url shortener service
            services.AddTransient<IUrlShortenerService, UrlShortenerService>(s => new UrlShortenerService(s.GetService<StorageDbContext>(), config.GetValue<string>("BaseUrl")));
        }

        public static void AddSessionStorage(this IServiceCollection services, IConfiguration config)
        {
            // Fetch the migration assembly
            var migrationsAssembly = typeof(StartupExtensions).GetTypeInfo().Assembly.GetName().Name;

            // Register the DB context
            services.AddDbContext<StorageDbContext>(options =>
                options.UseNpgsql(config.GetConnectionString("Database"), x => x.MigrationsAssembly(migrationsAssembly)));

            services.Configure<SessionStorageServiceOptions>(config);

            // Adds the session storage service
            services.AddTransient<ISessionStorageService, SessionStorageService>();
        }
    }
}