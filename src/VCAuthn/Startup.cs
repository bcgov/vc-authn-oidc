using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using VCAuthn.ACAPY;
using VCAuthn.IdentityServer;
using Swashbuckle.AspNetCore.Swagger;
using System.Collections.Generic;
using System.Linq;
using VCAuthn.Security;

namespace VCAuthn
{
    public class Startup
    {
        /// <summary>
        /// API version
        /// </summary>
        public static string ApiVersion = "v1";

        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = ApiKeyAuthenticationOptions.DefaultScheme;
                options.DefaultChallengeScheme = ApiKeyAuthenticationOptions.DefaultScheme;
            })
            .AddApiKeySupport(options => { });

            services.AddMvc()
                    .SetCompatibilityVersion(CompatibilityVersion.Version_2_2);

            // register ACAPY Client
            services.AddSingleton<IACAPYClient, ACAPYClient>(s => new ACAPYClient(Configuration.GetSection("ACAPY"), s.GetService<ILogger<ACAPYClient>>()));

            services.AddAuthServer(Configuration.GetSection("IdentityServer"));
            
            services.AddUrlShortenerService(Configuration.GetSection("UrlShortenerService"));
            services.AddSessionStorage(Configuration.GetSection("SessionStorageService"));

            //TODO enable running with ngrok

            //TODO add enable/disable swagger
            services.AddSwaggerGen(c =>
            {
                c.SwaggerDoc(ApiVersion, new Info { Title = "VC-Authn API", Version = ApiVersion });
                c.ResolveConflictingActions(apiDescriptions => apiDescriptions.First());
                c.AddSecurityDefinition("ApiKey",
                    new ApiKeyScheme
                    {
                        In = "header",
                        Description = "Please enter an API key",
                        Name = "X-Api-Key",
                        Type = "apiKey"
                    });
                c.AddSecurityRequirement(new Dictionary<string, IEnumerable<string>>
                    {
                        {"ApiKey", Enumerable.Empty<string>()}
                    });
                c.DescribeAllEnumsAsStrings();
            });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseStaticFiles();

            app.UseAuthentication();

            app.UseMvc();
            
            // Use the auth server
            app.UseAuthServer(Configuration.GetSection("IdentityServer"));

            // Enable middleware to serve generated Swagger as a JSON endpoint.
            app.UseSwagger();

            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint($"/swagger/{ApiVersion}/swagger.json", $"VC-Authn API {ApiVersion}");
            });
        }
    }
}
