using System;
using System.Collections.Specialized;
using System.Net;
using System.Threading.Tasks;
using IdentityModel;
using IdentityServer4.Endpoints.Results;
using IdentityServer4.Extensions;
using IdentityServer4.Hosting;
using IdentityServer4.Validation;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using VCAuthn.Services.Contracts;

namespace VCAuthn.IdentityServer.Endpoints
{
    public partial class TokenEndpoint : IEndpointHandler
    {
        private readonly IClientSecretValidator _clientValidator;
        private readonly ISessionStorageService _sessionStore;
        private readonly ITokenIssuerService _tokenIssuerService;
        private readonly IPresentationConfigurationService _presentationConfigurationService;
        private readonly ILogger<TokenEndpoint> _logger;

        public const string Name = "VCToken";

        public TokenEndpoint(IClientSecretValidator clientValidator, ISessionStorageService sessionStore, ITokenIssuerService tokenIssuerService, IPresentationConfigurationService presentationConfigurationService, ILogger<TokenEndpoint> logger)
        {
            _clientValidator = clientValidator;
            _sessionStore = sessionStore;
            _tokenIssuerService = tokenIssuerService;
            _presentationConfigurationService = presentationConfigurationService;
            _logger = logger;
        }

        public async Task<IEndpointResult> ProcessAsync(HttpContext context)
        {
            _logger.LogDebug($"Starting token request");

            NameValueCollection values;

            if (HttpMethods.IsPost(context.Request.Method))
            {
                if (!context.Request.HasFormContentType)
                {
                    _logger.LogDebug($"Unsupported media type");
                    return new StatusCodeResult(HttpStatusCode.UnsupportedMediaType);
                }

                values = context.Request.Form.AsNameValueCollection();
            }
            else
            {
                _logger.LogDebug($"Method not allowed");
                return new StatusCodeResult(HttpStatusCode.MethodNotAllowed);
            }

            var clientResult = await _clientValidator.ValidateAsync(context);
            if (clientResult.Client == null)
            {
                _logger.LogDebug($"Invalid client");
                return VCResponseHelpers.Error(OidcConstants.TokenErrors.InvalidClient);
            }

            var grantType = values.Get(IdentityConstants.GrantTypeParameterName);

            if (string.IsNullOrEmpty(grantType))
            {
                _logger.LogDebug($"Invalid grant type of : {grantType}");
                return VCResponseHelpers.Error(IdentityConstants.InvalidGrantTypeError);
            }

            var sessionId = values.Get(IdentityConstants.AuthorizationCodeParameterName);

            if (string.IsNullOrEmpty(sessionId))
            {
                _logger.LogDebug($"Invalid authorization code : {sessionId}");
                return VCResponseHelpers.Error(IdentityConstants.InvalidAuthorizationCodeError);
            }

            var session = await _sessionStore.FindBySessionIdAsync(sessionId);
            if (session == null)
            {
                _logger.LogDebug($"Invalid session : {sessionId}");
                return VCResponseHelpers.Error(IdentityConstants.InvalidSessionError, $"Cannot find stored session");
            }

            if (session.PresentationRequestSatisfied == false)
            {
                _logger.LogDebug($"Presentation not satisfied, session id : {sessionId}");
                return VCResponseHelpers.Error(IdentityConstants.InvalidSessionError, "Presentation request wasn't satisfied");
            }

            try
            {
                _logger.LogDebug($"Constructing token result for session : {sessionId}");
                return new TokenEndpointResult(session, _clientValidator, _tokenIssuerService, _presentationConfigurationService, _sessionStore, _logger);
            }
            catch (Exception e)
            {
                _logger.LogError(e, "Failed to create a token response");
                return VCResponseHelpers.Error(IdentityConstants.GeneralError, "Failed to create a token");
            }
        }
    }
}