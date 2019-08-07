using System.Linq;
using System.Reflection;
using IdentityServer4.EntityFramework.DbContexts;
using IdentityServer4.EntityFramework.Mappers;
using Microsoft.AspNetCore.Builder;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;

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
                .AddDeveloperSigningCredential(true, config.GetSection("CertificateFilename").Value);
        }
        
        public static void UseAuthServer(this IApplicationBuilder app, IConfiguration config)
        {
            InitializeDatabase(app, config.GetSection("RootClientSecret").Value);
            app.UseIdentityServer();
        }
        
         public static void InitializeDatabase(IApplicationBuilder app, string rootClientSecret)
        {
            using (var serviceScope = app.ApplicationServices.GetService<IServiceScopeFactory>().CreateScope())
            {
                //Resolve the required services
                var configContext = serviceScope.ServiceProvider.GetRequiredService<ConfigurationDbContext>();
                serviceScope.ServiceProvider.GetRequiredService<PersistedGrantDbContext>().Database.Migrate();

                //Migrate any required db contexts
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
                
                //Seed pre-configured clients
                var currentClients = configContext.Clients.ToList();
                foreach (var client in Config.GetClients())
                {
                    if (currentClients.Any(_ => _.ClientId == client.ClientId))
                    {
                        configContext.Clients.Update(client.ToEntity());
                    }
                    else
                    {
                        configContext.Clients.Add(client.ToEntity());
                    }
                }
                configContext.SaveChanges();
            }
        }
    }
}