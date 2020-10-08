using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Text.Encodings.Web;
using System.Threading.Tasks;

namespace VCAuthn.Security
{
    public class ApiKeyAuthenticationHandler : AuthenticationHandler<ApiKeyAuthenticationOptions>
    {
        private static Serilog.ILogger Log => Serilog.Log.ForContext<ApiKeyAuthenticationHandler>();
        private const string ProblemDetailsContentType = "application/problem+json";
        private readonly string _apiKey;
        private const string ApiKeyHeaderName = "X-Api-Key";
        public ApiKeyAuthenticationHandler(
            IOptionsMonitor<ApiKeyAuthenticationOptions> options,
            IConfiguration configuration,
            ILoggerFactory loggerFactory,
            UrlEncoder encoder,
            ISystemClock clock) : base(options, loggerFactory, encoder, clock)
        {
            _apiKey = configuration.GetValue<string>("ApiKey");
        }

        protected override Task<AuthenticateResult> HandleAuthenticateAsync()
        {
            Log.Debug($"Processing authentication request for {Request.Path.Value}.");

            if (string.IsNullOrEmpty(_apiKey))
            {
                Log.Debug("No API key configured.");
                return TaskSuccess();
            }

            if (!Request.Headers.TryGetValue(ApiKeyHeaderName, out var apiKeyHeaderValues))
            {
                Log.Debug("No matching request header found.");
                return Task.FromResult(AuthenticateResult.NoResult());
            }

            var providedApiKey = apiKeyHeaderValues.FirstOrDefault();
            if (apiKeyHeaderValues.Count == 0 || string.IsNullOrWhiteSpace(providedApiKey))
            {
                Log.Debug("No API key provided, or blank header.");
                return Task.FromResult(AuthenticateResult.NoResult());
            }

            if (providedApiKey.Equals(_apiKey))
            {
                Log.Debug("API key authentication succeeded, returning success.");
                return TaskSuccess();
            }

            return Task.FromResult(AuthenticateResult.Fail("Invalid API Key provided."));
        }

        private Task<AuthenticateResult> TaskSuccess()
        {
            var identity = new ClaimsIdentity(new List<Claim>(), Options.AuthenticationType);
            var identities = new List<ClaimsIdentity> { identity };
            var principal = new ClaimsPrincipal(identities);
            var ticket = new AuthenticationTicket(principal, Options.Scheme);

            return Task.FromResult(AuthenticateResult.Success(ticket));
        }

        // Customizes the 401 response
        protected override Task HandleChallengeAsync(AuthenticationProperties properties)
        {
            Response.StatusCode = 401;
            Response.ContentType = ProblemDetailsContentType;

            return Task.FromResult(false);
        }
    }
}
