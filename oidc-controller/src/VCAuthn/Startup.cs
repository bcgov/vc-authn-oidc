using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using VCAuthn.ACAPY;
using VCAuthn.IdentityServer;
using System.Collections.Generic;
using System.Linq;
using VCAuthn.Security;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;

namespace VCAuthn
{
    public class Startup
    {
        /// <summary>
        /// API version
        /// </summary>
        public static string ApiVersion = "v1";

        private readonly ILogger<Startup> _logger;

        public Startup(IConfiguration configuration, ILogger<Startup> logger)
        {
            Configuration = configuration;
            _logger = logger;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.Configure<ForwardedHeadersOptions>(options =>
            {
                options.ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto | ForwardedHeaders.XForwardedHost;
                options.KnownNetworks.Clear();
                options.KnownProxies.Clear();
            });

            services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = ApiKeyAuthenticationOptions.DefaultScheme;
                options.DefaultChallengeScheme = ApiKeyAuthenticationOptions.DefaultScheme;
            })
            .AddApiKeySupport();

            services.AddMvc();

            // register ACAPY Client
            services.AddSingleton<IACAPYClient, ACAPYClient>(s => new ACAPYClient(Configuration.GetSection("ACAPY"), s.GetService<ILogger<ACAPYClient>>()));

            services.AddAuthServer(Configuration.GetSection("IdentityServer"));

            services.AddUrlShortenerService(Configuration.GetSection("UrlShortenerService"));

            services.AddSessionStorage(Configuration.GetSection("SessionStorageService"));

            if (Configuration.GetValue<bool>("SwaggerEnabled"))
            {
                _logger.LogDebug("Enabling SwaggerUI");

                services.AddSwaggerGen(c =>
                {
                    c.SwaggerDoc(ApiVersion, new OpenApiInfo { Title = "VC-Authn API", Version = ApiVersion });
                    c.ResolveConflictingActions(apiDescriptions => apiDescriptions.First());
                    c.AddSecurityDefinition("ApiKey",
                        new OpenApiSecurityScheme
                        {
                            In = ParameterLocation.Header,
                            Description = "Controller API Key",
                            Name = "X-Api-Key",
                            Type = SecuritySchemeType.ApiKey
                        });
                    c.AddSecurityRequirement(new OpenApiSecurityRequirement{
                        {
                            new OpenApiSecurityScheme{
                                Reference = new OpenApiReference{
                                    Type = ReferenceType.SecurityScheme,
                                    Id = "ApiKey"
                                }
                            },new List<string>()
                        }
                    });
                });
            }

            // enable NewtonSoft.Json support for SwashBuckle
            services.AddSwaggerGenNewtonsoftSupport();

            // replace System.Text.Json with NewtonSoft.Json
            services.AddControllers().AddNewtonsoftJson();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseStaticFiles();
            app.UseAuthentication();
            app.UseRouting();
            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapRazorPages();
                endpoints.MapControllers();
            });

            // Use the auth server
            app.UseAuthServer(Configuration.GetSection("IdentityServer"));

            // Enable middleware to serve generated Swagger as a JSON endpoint.
            app.UseSwagger();

            // Enable middleware to serve swagger-ui (HTML, JS, CSS, etc.),
            // specifying the Swagger JSON endpoint.
            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint($"/swagger/{ApiVersion}/swagger.json", $"VC-Authn API {ApiVersion}");
            });
        }
    }
}
