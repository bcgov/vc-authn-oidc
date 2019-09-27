using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Net;
using System.Security.Claims;
using System.Threading.Tasks;
using IdentityModel;
using IdentityServer4.Endpoints.Results;
using IdentityServer4.Extensions;
using IdentityServer4.Hosting;
using IdentityServer4.Validation;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using VCAuthn.IdentityServer.SessionStorage;
using VCAuthn.PresentationConfiguration;

namespace VCAuthn.IdentityServer.Endpoints
{
    public class TokenEndpoint : IEndpointHandler
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
            NameValueCollection values;

            if (HttpMethods.IsPost(context.Request.Method))
            {
                if (!context.Request.HasFormContentType)
                {
                    return new StatusCodeResult(HttpStatusCode.UnsupportedMediaType);
                }

                values = context.Request.Form.AsNameValueCollection();
            }
            else
            {
                return new StatusCodeResult(HttpStatusCode.MethodNotAllowed);
            }

            var clientResult = await _clientValidator.ValidateAsync(context);
            if (clientResult.Client == null)
            {
                return VCResponseHelpers.Error(OidcConstants.TokenErrors.InvalidClient);
            }

            var grantType = values.Get(IdentityConstants.GrantTypeParameterName);

            if (string.IsNullOrEmpty(grantType))
            {
                return VCResponseHelpers.Error(IdentityConstants.InvalidGrantTypeError);
            }

            var sessionId = values.Get(IdentityConstants.AuthorizationCodeParameterName);

            if (string.IsNullOrEmpty(sessionId))
                return VCResponseHelpers.Error(IdentityConstants.InvalidAuthorizationCodeError);

            var session = await _sessionStore.FindBySessionIdAsync(sessionId);
            if (session == null)
            {
                return VCResponseHelpers.Error(IdentityConstants.InvalidSessionError, $"Cannot find stored session");
            }

            if (session.PresentationRequestSatisfied == false)
            {
                return VCResponseHelpers.Error(IdentityConstants.InvalidSessionError, "Presentation request wasn't satisfied");
            }

            try
            {
                return new TokenResult(session, _tokenIssuerService, _presentationConfigurationService, _sessionStore, _logger);
            }
            catch (Exception e)
            {
                _logger.LogError(e, "Failed to create a token response");
                return VCResponseHelpers.Error(IdentityConstants.GeneralError, "Failed to create a token");
            }
        }

        public class TokenResult : IEndpointResult
        {
            private readonly AuthSession _session;
            private readonly ITokenIssuerService _tokenIssuerService;
            private readonly IPresentationConfigurationService _presentationConfigurationService;
            private readonly ISessionStorageService _sessionStorage;
            private readonly ILogger _logger;

            public TokenResult(AuthSession session, ITokenIssuerService tokenIssuerService, IPresentationConfigurationService presentationConfigurationService, ISessionStorageService sessionStorage, ILogger logger)
            {
                _session = session;
                _tokenIssuerService = tokenIssuerService;
                _presentationConfigurationService = presentationConfigurationService;
                _sessionStorage = sessionStorage;
                _logger = logger;
            }

            public async Task ExecuteAsync(HttpContext context)
            {
                var issuer = context.GetIdentityServerIssuerUri();

                var audience = _session.RequestParameters.ContainsKey(IdentityConstants.ClientId) ? _session.RequestParameters[IdentityConstants.ClientId] : "";

                var token = await _tokenIssuerService.IssueJwtAsync(10000, issuer, new string[] { audience }, await GetClaims());

                if (_sessionStorage.DeleteSession(_session) == false)
                {
                    _logger.LogError("Failed to delete a session");
                }

                await context.Response.WriteJsonAsync(new
                {
                    access_token = "invalid",
                    id_token = token,
                    token_type = "Bearer"
                });
            }

            private async Task<List<Claim>> GetClaims()
            {
                var claims = new List<Claim>
                {
                    new Claim(IdentityConstants.PresentationRequestConfigIDParamName, _session.PresentationRecordId),
                    new Claim(IdentityConstants.AuthenticationContextReferenceIdentityTokenKey, IdentityConstants.VCAuthnScopeName)
                };

                var presentationConfig = await _presentationConfigurationService.GetAsync(_session.PresentationRecordId);

                if (_session.RequestParameters.ContainsKey(IdentityConstants.NonceParameterName))
                {
                    claims.Add(new Claim(IdentityConstants.NonceParameterName, _session.RequestParameters[IdentityConstants.NonceParameterName]));
                }

                foreach (var requestedAttr in _session.PresentationRequest.RequestedAttributes)
                {
                    if (_session.Presentation.RequestedProof.RevealedAttributes.ContainsKey(requestedAttr.Key))
                    {
                        claims.Add(new Claim(requestedAttr.Value.Name, _session.Presentation.RequestedProof.RevealedAttributes[requestedAttr.Key].Raw));
                        if (!string.IsNullOrEmpty(presentationConfig.SubjectIdentifier) && string.Equals(requestedAttr.Value.Name, presentationConfig.SubjectIdentifier, StringComparison.InvariantCultureIgnoreCase))
                        {
                            claims.Add(new Claim(IdentityConstants.SubjectIdentityTokenKey, _session.Presentation.RequestedProof.RevealedAttributes[requestedAttr.Key].Raw));
                        }
                    }
                }

                if (!claims.Any(_ => _.Type == IdentityConstants.SubjectIdentityTokenKey))
                {
                    claims.Add(new Claim(IdentityConstants.SubjectIdentityTokenKey, Guid.NewGuid().ToString()));
                }

                return claims;
            }
        }
    }
}