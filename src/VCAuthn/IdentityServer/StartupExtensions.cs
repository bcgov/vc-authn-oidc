using System.Linq;
using System.Reflection;
using IdentityServer4.EntityFramework.DbContexts;
using IdentityServer4.EntityFramework.Mappers;
using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using VCAuthn.IdentityServer.Endpoints;
using VCAuthn.IdentityServer.SessionStorage;
using VCAuthn.PresentationConfiguration;
using VCAuthn.UrlShortener;
using VCAuthn.Utils;

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

                    // When forwarded headers aren't sufficient we leverage PublicOrigin option
                    options.PublicOrigin = config.GetSection("PublicOrigin").Value;
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
                
                // If cert supplied will parse and call AddSigningCredential(), if not found will create a temp one
                .AddDeveloperSigningCredential(true, config.GetSection("CertificateFilename").Value)
                
                // Custom Endpoints
                .AddEndpoint<AuthorizeEndpoint>(AuthorizeEndpoint.Name, IdentityConstants.VerifiedCredentialAuthorizeUri.EnsureLeadingSlash())
                ;
            
            services.AddSingleton<IPresentationConfigurationService, PresentationConfigurationService>();
            
        }
        
        public static void UseAuthServer(this IApplicationBuilder app, IConfiguration config)
        {
            InitializeDatabase(app, config.GetSection("RootClientSecret").Value);
            app.UseIdentityServer();
        }
        
        public static void InitializeDatabase(IApplicationBuilder app, string rootClientSecret)
        {
            var _logger = app.ApplicationServices.GetService<ILogger<Startup>>();
            
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
                
                foreach (var client in Config.GetClients())
                {
                    if (currentClients.All(_ => _.ClientId != client.ClientId))
                    {
                        _logger.LogDebug($"Inserting client [{client.ClientId}]");
                        configContext.Clients.Add(client.ToEntity());    configContext.SaveChanges();
                    }
                }
                configContext.SaveChanges();
            }
        }
        
        public static void AddUrlShortenerService(this IServiceCollection services, IConfiguration config)
        {
            // Fetch the migration assembly
            var migrationsAssembly = typeof(StartupExtensions).GetTypeInfo().Assembly.GetName().Name;

            // Register the DB context
            services.AddDbContext<UrlShortenerServiceDbContext>(options =>
                options.UseNpgsql(config.GetConnectionString("Database"), x => x.MigrationsAssembly(migrationsAssembly)));

            // Adds the url shortner service
            services.AddTransient<IUrlShortenerService, UrlShortenerService>(s => new UrlShortenerService(s.GetService<UrlShortenerServiceDbContext>(), config.GetValue<string>("BaseUrl")));
        }
        
        public static void UseUrlShortenerService(this IApplicationBuilder app)
        {
            using (var serviceScope = app.ApplicationServices.GetService<IServiceScopeFactory>().CreateScope())
            {
                var context = serviceScope.ServiceProvider.GetService<UrlShortenerServiceDbContext>();
                context.Database.Migrate();
            }
        }
        
        
        public static void AddSessionStorage(this IServiceCollection services, IConfiguration config)
        {
            // Fetch the migration assembly
            var migrationsAssembly = typeof(StartupExtensions).GetTypeInfo().Assembly.GetName().Name;

            // Register the DB context
            services.AddDbContext<SessionStorageDbContext>(options =>
                options.UseNpgsql(config.GetConnectionString("Database"), x => x.MigrationsAssembly(migrationsAssembly)));

            services.Configure<SessionStorageServiceOptions>(config);
            
            // Adds the session storage service
            services.AddTransient<ISessionStorageService, SessionStorageService>();
        }
        
        public static void UseSessionStorage(this IApplicationBuilder app)
        {
            using (var serviceScope = app.ApplicationServices.GetService<IServiceScopeFactory>().CreateScope())
            {
                var context = serviceScope.ServiceProvider.GetService<SessionStorageDbContext>();
                context.Database.Migrate();
            }
        }
    }
}