using System.Linq;
using System.Threading.Tasks;
using IdentityModel;
using IdentityServer4;
using IdentityServer4.Configuration;
using IdentityServer4.Models;
using IdentityServer4.Validation;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace VCAuthn.IdentityServer
{
    public class QueryStringSecretParser : ISecretParser
    {
        private readonly IdentityServerOptions _options;
        private static Serilog.ILogger Log => Serilog.Log.ForContext<QueryStringSecretParser>();

        public QueryStringSecretParser(IdentityServerOptions options)
        {
            _options = options;
        }
        
        public string AuthenticationMethod => "client_secret_query";

        public async Task<ParsedSecret> ParseAsync(HttpContext context)
        {
            Log.Debug("Start parsing for secret in query string");

            var query = context.Request.Query;

            if (query == null)
            {
                Log.Debug("No secret in query string found");
                return null;
            }

            var id = query["client_id"].FirstOrDefault();
            var secret = query["client_secret"].FirstOrDefault();

            // client id must be present
            if (string.IsNullOrEmpty(id))
            {
                Log.Debug("No client_id in query string found");
                return null;
            }
            
            if (id.Length > _options.InputLengthRestrictions.ClientId)
            {
                Log.Error($"Client id exceeds maximum length of { _options.InputLengthRestrictions.ClientId}");
                return null;
            }

            if (string.IsNullOrEmpty(secret))
            {
                // client secret is optional
                Log.Debug("client id without secret found");

                return new ParsedSecret
                {
                    Id = id,
                    Type = IdentityServerConstants.ParsedSecretTypes.NoSecret
                };
            }
            
            if (secret.Length > _options.InputLengthRestrictions.ClientSecret)
            {
                Log.Error("Client secret exceeds maximum length.");
                return null;
            }

            return new ParsedSecret
            {
                Id = id,
                Credential = secret,
                Type = IdentityServerConstants.ParsedSecretTypes.SharedSecret
            };
        }
    }
}