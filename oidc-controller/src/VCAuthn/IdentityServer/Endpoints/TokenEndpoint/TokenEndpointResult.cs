using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using IdentityServer4.Extensions;
using IdentityServer4.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using VCAuthn.Models;
using VCAuthn.Services.Contracts;
using VCAuthn.Utils;
using Newtonsoft.Json;

namespace VCAuthn.IdentityServer.Endpoints
{
    public partial class TokenEndpoint
    {
        public class TokenEndpointResult : IEndpointResult
        {
            private readonly AuthSession _session;
            private readonly ITokenIssuerService _tokenIssuerService;
            private readonly IPresentationConfigurationService _presentationConfigurationService;
            private readonly ISessionStorageService _sessionStorage;
            private readonly ILogger _logger;

            public TokenEndpointResult(AuthSession session, ITokenIssuerService tokenIssuerService, IPresentationConfigurationService presentationConfigurationService, ISessionStorageService sessionStorage, ILogger logger)
            {
                _session = session;
                _tokenIssuerService = tokenIssuerService;
                _presentationConfigurationService = presentationConfigurationService;
                _sessionStorage = sessionStorage;
                _logger = logger;
            }

            public async Task ExecuteAsync(HttpContext context)
            {
                _logger.LogDebug("Constructing token result");

                var issuer = context.GetIdentityServerIssuerUri();

                var audience = _session.RequestParameters.ContainsKey(IdentityConstants.ClientId) ? _session.RequestParameters[IdentityConstants.ClientId] : "";

                _logger.LogDebug($"Generating token for audience : {audience}");

                var token = await _tokenIssuerService.IssueJwtAsync(10000, issuer, new string[] { audience }, await GetClaims());

                _logger.LogDebug($"Token created, invalidating session");

                if (_sessionStorage.DeleteSession(_session) == false)
                {
                    _logger.LogError("Failed to delete a session");
                }

                _logger.LogDebug($"Returning token result");

                await context.Response.WriteJsonAsync(new
                {
                    access_token = "invalid",
                    id_token = token,
                    token_type = "Bearer"
                });
            }

            private async Task<List<Claim>> GetClaims()
            {
                _logger.LogDebug($"Creating Claims list for presentation record id : {_session.PresentationRecordId}");

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

                PresentationRequest presentationRequest = JsonConvert.DeserializeObject<PresentationRequest>(_session.PresentationRequest);
                foreach (var requestedAttr in presentationRequest.RequestedAttributes)
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

                // Add "issued at" standard OIDC claim - see https://tools.ietf.org/html/rfc7519#section-4
                claims.Add(new Claim(IdentityConstants.OIDCTokenIssuedAt, DateTimeOffset.Now.ToUnixTimeSeconds().ToString(), System.Security.Claims.ClaimValueTypes.Integer));

                _logger.LogDebug($"Claims list created for presentation record id : {_session.PresentationRecordId}, values : {claims.ToJson()}");

                return claims;
            }
        }
    }
}