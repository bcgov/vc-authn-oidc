using System;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using IdentityServer4.Endpoints.Results;
using IdentityServer4.Extensions;
using IdentityServer4.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using VCAuthn.IdentityServer.SessionStorage;

namespace VCAuthn.IdentityServer.Endpoints
{
    public class AuthorizeCallback : IEndpointHandler
    {
        public const string Name = "VCAuthorizeCallback";
        
        private readonly ISessionStorageService _sessionStorageService;
        private readonly ITokenIssuerService _tokenIssuerService;
        private readonly ILogger<AuthorizeCallback> _logger;

        public AuthorizeCallback(ISessionStorageService sessionStorageService, ITokenIssuerService tokenIssuerService, ILogger<AuthorizeCallback> logger)
        {
            _sessionStorageService = sessionStorageService;
            _tokenIssuerService = tokenIssuerService;
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
                
                return new RedirectResult(url);
            }

            //if (session.RequestParameters[IdentityConstants.ResponseTypeUriParameterName] == "token")
            //{
            //    _logger.LogDebug("Token flow. Creating a token");
            //    var presentation = session.Presentation;
            //    var issuer = context.GetIdentityServerIssuerUri();
            //    var token = await _tokenIssuerService.IssueJwtAsync(10000, issuer, session.PresentationRecordId, presentation); //TODO parameterize token issuance

            //    if (_sessionStorageService.DeleteSession(session) == false)
            //    {
            //        _logger.LogError("Failed to delete a session");
            //    }

            //    var url = $"{session.RequestParameters[IdentityConstants.RedirectUriParameterName]}#access_token ={token}&token_type=Bearer";
            //    _logger.LogDebug($"Token flow. Redirecting to {url}");

            //    return new RedirectResult(url);
            //}

            _logger.LogError("Unknown response type");
            return VCResponseHelpers.Error("invalid_response_type", $"Unknown response type: [{session.RequestParameters[IdentityConstants.ResponseModeUriParameterName]}]");
        }


        public class RedirectResult : IEndpointResult
        {
            private readonly string _url;
            
            public RedirectResult(string url)
            {
                if (string.IsNullOrWhiteSpace(url)) throw new ArgumentNullException(nameof(url));

                _url = url;
            }

            public async Task ExecuteAsync(HttpContext context)
            {
                context.Response.RedirectToAbsoluteUrl(_url);

                await Task.CompletedTask;
            }
        }
    }
}