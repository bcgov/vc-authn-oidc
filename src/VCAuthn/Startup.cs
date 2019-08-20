using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using VCAuthn.ACAPY;
using VCAuthn.IdentityServer;

namespace VCAuthn
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddMvc().SetCompatibilityVersion(CompatibilityVersion.Version_2_2);

            // register ACAPY Client
            services.AddSingleton<IACAPYClient, ACAPYClient>(s => new ACAPYClient(Configuration.GetSection("ACAPY"), s.GetService<ILogger<ACAPYClient>>()));;
            
            services.AddAuthServer(Configuration.GetSection("IdentityServer"));
            
            services.AddUrlShortenerService(Configuration.GetSection("UrlShortenerService"));
            services.AddSessionStorage(Configuration.GetSection("SessionStorageService"));

        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseStaticFiles();

            app.UseMvc();
            
            // Use the auth server
            app.UseAuthServer(Configuration.GetSection("IdentityServer"));

            app.UseUrlShortenerService();
            app.UseSessionStorage();
        }
    }
}
