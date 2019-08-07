using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace VCAuthn
{
    public class Program
    {
        public static void Main(string[] args)
        {
            CreateWebHostBuilder(args).Build().Run();
        }

        public static IWebHostBuilder CreateWebHostBuilder(string[] args)
        {
            var config = new ConfigurationBuilder()
                .AddCommandLine(args)
                .AddEnvironmentVariables()
                .Build();
            
            return WebHost.CreateDefaultBuilder(args)
                .UseConfiguration(config)
                .ConfigureLogging((hostingContext, logging) =>
                {
                    logging.ClearProviders(); // to clear CreateDefaultBuilder's setup of standard debug and console loggers, rely on log4net exclusively
                    logging.AddLog4Net();
                    logging.AddConfiguration(hostingContext.Configuration.GetSection("Logging"));
                    log4net.GlobalContext.Properties["CorrelationId"] = ""; // default to empty string, set via LoggingMiddleware per request
                })
                .UseStartup<Startup>();
        }
            
    }
}
