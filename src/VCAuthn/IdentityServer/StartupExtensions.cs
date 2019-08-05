using System.Reflection;
using Microsoft.AspNetCore.Builder;
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
//                .AddConfigurationStore(options =>
//                {
//                    options.ConfigureDbContext = b =>
//                        b.UseNpgsql(connectionString,
//                            sql => sql.MigrationsAssembly(migrationsAssembly));
//                })
//                .AddOperationalStore(options =>
//                {
//                    options.ConfigureDbContext = b =>
//                        b.UseNpgsql(connectionString,
//                            sql => sql.MigrationsAssembly(migrationsAssembly));
//                    // this enables automatic token cleanup. this is optional.
//                    options.EnableTokenCleanup = true;
//                })

                
                // If cert supplied will parse and call AddSigningCredential(), if not found will create a temp one
                .AddDeveloperSigningCredential(true, config.GetSection("CertificateFilename").Value)
                
                .AddInMemoryIdentityResources(Config.GetIdentityResources())
                .AddInMemoryClients(Config.GetClients());
                ;
        }
        
        public static void UseAuthServer(this IApplicationBuilder app, IConfiguration config)
        {
            app.UseIdentityServer();
        }
    }
}