using System;
using System.Collections.Generic;
using System.Security.Claims;
using System.Threading.Tasks;
using IdentityModel;
using IdentityServer4.Models;
using IdentityServer4.Services;
using Microsoft.AspNetCore.Authentication;
using VCAuthn.IdentityServer.SessionStorage;
using VCAuthn.PresentationConfiguration;

namespace VCAuthn.IdentityServer.Endpoints
{
    /// <summary>
    /// A token issuer service.
    /// </summary>
    public interface ITokenIssuerService
    {
        /// <summary>
        /// Issues a JWT.
        /// </summary>
        Task<string> IssueJwtAsync(int lifetime, string issuer, string presentationRecordId, PartialPresentation presentation);
    }

    public class TokenIssuerService : ITokenIssuerService
    {
        private readonly ITokenCreationService _tokenCreation;
        private readonly ISystemClock _clock;
        private readonly IPresentationConfigurationService _presentationConfigurationService;

        public TokenIssuerService(ITokenCreationService tokenCreation, ISystemClock clock, IPresentationConfigurationService presentationConfigurationService)
        {
            _tokenCreation = tokenCreation;
            _clock = clock;
            _presentationConfigurationService = presentationConfigurationService;
        }

        public async Task<string> IssueJwtAsync(int lifetime, string issuer, string presentationRecordId, PartialPresentation presentation)
        {
            var claims = new List<Claim>
            {
                new Claim(IdentityConstants.PresentationRequestConfigIDParamName, presentationRecordId),
                new Claim("amr", IdentityConstants.VCAuthnScopeName)
            };

            var presentationConfig = await _presentationConfigurationService.GetAsync(presentationRecordId);

            foreach (var attr in presentation.RequestedProof.RevealedAttributes)
            {
                claims.Add(new Claim(attr.Key, attr.Value.Raw));
                if (string.Equals(attr.Key, presentationConfig.SubjectIdentifier, StringComparison.InvariantCultureIgnoreCase))
                {
                    claims.Add(new Claim("sub", attr.Value.Raw));
                }
            }

            var token = new Token
            {
                CreationTime = _clock.UtcNow.UtcDateTime,
                Issuer = issuer,
                Lifetime = lifetime,
                Claims = new HashSet<Claim>(claims, new ClaimComparer())
            };

            return await _tokenCreation.CreateTokenAsync(token);
        }
    }
}