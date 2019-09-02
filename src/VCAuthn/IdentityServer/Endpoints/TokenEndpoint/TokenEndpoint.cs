using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Net;
using System.Security.Claims;
using System.Threading.Tasks;
using IdentityModel;
using IdentityServer4.Endpoints.Results;
using IdentityServer4.Extensions;
using IdentityServer4.Hosting;
using IdentityServer4.Models;
using IdentityServer4.Services;
using IdentityServer4.Validation;
using log4net;
using Microsoft.AspNetCore.Authentication;
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
        private readonly ILogger _logger;

        public const string Name = "VCToken";

        public TokenEndpoint(IClientSecretValidator clientValidator, ISessionStorageService sessionStore, ITokenIssuerService tokenIssuerService, IPresentationConfigurationService presentationConfigurationService, ILogger logger)
        {
            _clientValidator = clientValidator;
            _sessionStore = sessionStore;
            _tokenIssuerService = tokenIssuerService;
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

            if (grantType != IdentityConstants.VerificationCodeGrantType)
            {
                return VCResponseHelpers.Error(IdentityConstants.InvalidGrantTypeError);
            }

            var sessionId = values.Get(IdentityConstants.VerificationCodeParameterName);

            if (string.IsNullOrEmpty(sessionId))
                return VCResponseHelpers.Error(IdentityConstants.InvalidVerificationCodeError);

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
                return new TokenResult(session, _tokenIssuerService, _sessionStore, _logger);
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
            private readonly ISessionStorageService _sessionStorage;
            private readonly ILogger _logger;

            public TokenResult(AuthSession session, ITokenIssuerService tokenIssuerService, ISessionStorageService sessionStorage, ILogger logger)
            {
                _session = session;
                _tokenIssuerService = tokenIssuerService;
                _sessionStorage = sessionStorage;
                _logger = logger;
            }

            public async Task ExecuteAsync(HttpContext context)
            {
                var presentation = _session.Presentation;
                var issuer = context.GetIdentityServerIssuerUri();
                var token = await _tokenIssuerService.IssueJwtAsync(10000, issuer, _session.PresentationRecordId, presentation);

                if (_sessionStorage.DeleteSession(_session) == false)
                {
                    _logger.LogError("Failed to delete a session");
                }

                await context.Response.WriteJsonAsync(new
                {
                    access_token = token,
                    token_type = "Bearer"
                });
            }
        }
    }
}