using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Net;
using System.Threading.Tasks;
using IdentityModel;
using IdentityServer4.Configuration;
using IdentityServer4.Hosting;
using IdentityServer4.Validation;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Newtonsoft.Json;
using VCAuthn.ACAPY;
using VCAuthn.IdentityServer.SessionStorage;
using VCAuthn.PresentationConfiguration;
using VCAuthn.UrlShortener;
using VCAuthn.Utils;
using StatusCodeResult = IdentityServer4.Endpoints.Results.StatusCodeResult;

namespace VCAuthn.IdentityServer.Endpoints
{
    public class AuthorizeEndpoint : IEndpointHandler
    {
        public const string Name = "VCAuthorize";
        
        private readonly IClientSecretValidator _clientValidator;
        private readonly IPresentationConfigurationService _presentationConfigurationService;
        private readonly IUrlShortenerService _urlShortenerService;
        private readonly ISessionStorageService _sessionStorage;
        private readonly IACAPYClient _acapyClient;
        private readonly IdentityServerOptions _options;
        private readonly ILogger _logger;

        public AuthorizeEndpoint(
            IClientSecretValidator clientValidator,
            IPresentationConfigurationService presentationConfigurationService,
            IUrlShortenerService urlShortenerService,
            ISessionStorageService sessionStorage,
            IACAPYClient acapyClient,
            IOptions<IdentityServerOptions> options,
            ILogger<AuthorizeEndpoint> logger
            )
        {
            _clientValidator = clientValidator;
            _presentationConfigurationService = presentationConfigurationService;
            _urlShortenerService = urlShortenerService;
            _sessionStorage = sessionStorage;
            _acapyClient = acapyClient;
            _options = options.Value;
            _logger = logger;
        }
        
        public async Task<IEndpointResult> ProcessAsync(HttpContext context)
        {
            _logger.LogDebug("Processing Authorize request");

            NameValueCollection values;
            switch (context.Request.Method)
            {
                case "GET":
                    values = context.Request.Query.AsNameValueCollection();
                    break;
                case "POST":
                    if (!context.Request.HasFormContentType)
                    {
                        return new StatusCodeResult(HttpStatusCode.UnsupportedMediaType);
                    }
                    values = context.Request.Form.AsNameValueCollection();
                    break;
                default:
                    return new StatusCodeResult(HttpStatusCode.MethodNotAllowed);
            }

            var clientResult = await _clientValidator.ValidateAsync(context);
            if (clientResult.Client == null)
            {
                return VCResponseHelpers.Error(OidcConstants.TokenErrors.InvalidClient);
            }

            var scopes = values.Get(IdentityConstants.ScopeParamName).Split(' ');
            if (!scopes.Contains(IdentityConstants.VCAuthnScopeName))
            {
                return VCResponseHelpers.Error(IdentityConstants.MissingVCAuthnScopeError, IdentityConstants.MissingVCAuthnScopeDesc);
            }
            
            var presentationRecordId = values.Get(IdentityConstants.PresentationRequestConfigIDParamName);
            if (string.IsNullOrEmpty(presentationRecordId))
            {
                return VCResponseHelpers.Error(IdentityConstants.InvalidPresentationRequestConfigIDError, IdentityConstants.InvalidPresentationRequestConfigIDDesc);
            }
            
            var redirectUrl = values.Get(IdentityConstants.RedirectUriParameterName);
            if (string.IsNullOrEmpty(redirectUrl))
            {
                return VCResponseHelpers.Error(IdentityConstants.InvalidRedirectUriError);
            }
            
            if (clientResult.Client.RedirectUris.Any() && !clientResult.Client.RedirectUris.Contains(redirectUrl))
            {
                return VCResponseHelpers.Error(IdentityConstants.InvalidRedirectUriError);
            }
            
            var responseType = values.Get(IdentityConstants.ResponseTypeUriParameterName);
            if (string.IsNullOrEmpty(responseType))
            {
                responseType = IdentityConstants.DefaultResponseType;
            }

            var responseMode = values.Get(IdentityConstants.ResponseModeUriParameterName);
            if (string.IsNullOrEmpty(responseMode))
            {
                responseMode = IdentityConstants.DefaultResponseMode;
            }

            PresentationRecord presentationRecord;
            try
            {
                presentationRecord = await _presentationConfigurationService.GetAsync(presentationRecordId);
            }
            catch (Exception)
            {
                return VCResponseHelpers.Error(IdentityConstants.UnknownPresentationRecordId, "Cannot find respective record id");
            }

            WalletPublicDid acapyPublicDid;
            try
            {
                acapyPublicDid = await _acapyClient.WalletDidPublic();
            }
            catch (Exception e)
            {
                _logger.LogError(e, "Cannot fetch ACAPy wallet public did");
                return VCResponseHelpers.Error(IdentityConstants.AcapyCallFailed, "Cannot fetch ACAPy wallet public did");
            }

            var presentationRequest = BuildPresentationRequest(presentationRecord, acapyPublicDid);
            
            // create a full and short url versions of a presentation requests
            string shortUrl;
            try
            {
                var url = string.Format("{0}?m={1}", _options.PublicOrigin, presentationRequest.ToJson().ToBase64());
                shortUrl = await _urlShortenerService.CreateShortUrlAsync(url);
            }
            catch (Exception e)
            {
                _logger.LogError(e, "Presentation url build failed");
                return VCResponseHelpers.Error(IdentityConstants.PresentationUrlBuildFailed, "Presentation url build failed");
            }

            // persist presentation request details in session
            try
            {
                var session = await _sessionStorage.CreateSessionAsync(new AuthSession(){
                    PresentationRequestId = presentationRequest.Id, 
                    PresentationRecordId = presentationRecordId,
                    ResponseType = responseType,
                    RedirectUrl = redirectUrl
                });

                // set up a session cookie
                context.Response.Cookies.Append(IdentityConstants.SessionIdCookieName, session.Id);
            }
            catch (Exception)
            {
                return VCResponseHelpers.Error(IdentityConstants.SessionStartFailed, "Failed to start a new session");
            }

            return new AuthorizationEndpointResult(
                new AuthorizationViewModel(
                    shortUrl, 
                    $"{_options.PublicOrigin}/{IdentityConstants.VerificationChallengePollUri}?{IdentityConstants.ChallengeIdQueryParameterName}={presentationRequest.Id}", 
                    $"{_options.PublicOrigin}/{IdentityConstants.AuthorizeCallbackUri}?{IdentityConstants.ChallengeIdQueryParameterName}={presentationRequest.Id}"));
        }

        private PresentationRequest BuildPresentationRequest(PresentationRecord record, WalletPublicDid acapyPublicDid)
        {
            record.Configuration.Nonce = $"0{Guid.NewGuid().ToString("N")}";

            var request = new PresentationRequest
            {
                Id = Guid.NewGuid().ToString(),
                Request = record.Configuration,
                Service = new ServiceDecorator
                {
                    RecipientKeys = new List<string>{acapyPublicDid.Verkey},
                    ServiceEndpoint = _acapyClient.GetServicePublicUrl()
                }
            };
            return request;
        }
    }
}