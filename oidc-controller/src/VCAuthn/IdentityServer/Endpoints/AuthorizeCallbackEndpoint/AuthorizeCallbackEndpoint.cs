using System.Linq;
using System.Net;
using System.Threading.Tasks;
using IdentityServer4.Endpoints.Results;
using IdentityServer4.Extensions;
using IdentityServer4.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using VCAuthn.Services.Contracts;

namespace VCAuthn.IdentityServer.Endpoints.AuthorizeCallbackEndpoint
{
    public class AuthorizeCallbackEndpoint : IEndpointHandler
    {
        public const string Name = "VCAuthorizeCallback";
        
        private readonly ISessionStorageService _sessionStorageService;
        private readonly ILogger<AuthorizeCallbackEndpoint> _logger;

        public AuthorizeCallbackEndpoint(ISessionStorageService sessionStorageService, ILogger<AuthorizeCallbackEndpoint> logger)
        {
            _sessionStorageService = sessionStorageService;
            _logger = logger;
        }
        
        public async Task<IEndpointResult> ProcessAsync(HttpContext context)
        {
            if (!HttpMethods.IsGet(context.Request.Method))
            {
                _logger.LogDebug($"Invalid HTTP method for authorize endpoint. Method: [{context.Request.Method}]");
                return  new StatusCodeResult(HttpStatusCode.UnsupportedMediaType);
            }
            
            _logger.LogDebug("Start authorize callback request");
                
            var sessionParam = context.Request.Query[IdentityConstants.ChallengeIdQueryParameterName];
            if (sessionParam.IsNullOrEmpty() || string.IsNullOrEmpty(sessionParam.FirstOrDefault()))
            {
                return VCResponseHelpers.Error("missing_session", $"Empty {IdentityConstants.ChallengeIdQueryParameterName} param");
            }
            var sessionId = sessionParam.FirstOrDefault();

            var session = await _sessionStorageService.FindByPresentationIdAsync(sessionId);
            if (session == null)
            {
                return VCResponseHelpers.Error("invalid_session", "Cannot find corresponding session");
            }

            if (session.RequestParameters[IdentityConstants.ResponseTypeUriParameterName] == "code")
            {
                var url = $"{session.RequestParameters[IdentityConstants.RedirectUriParameterName]}?code={session.Id}";

                if (session.RequestParameters.ContainsKey(IdentityConstants.StateParameterName))
                    url += $"&state={session.RequestParameters[IdentityConstants.StateParameterName]}";

                _logger.LogDebug($"Code flow. Redirecting to {url}");
                
                return new AuthorizeCallbackResult(url);
            }

            //TODO add token flow handling

            _logger.LogError("Unknown response type");
            return VCResponseHelpers.Error("invalid_response_type", $"Unknown response type: [{session.RequestParameters[IdentityConstants.ResponseModeUriParameterName]}]");
        }
    }
}