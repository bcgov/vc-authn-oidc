using System.Collections.Generic;
using System.Security.Claims;
using System.Threading.Tasks;
using IdentityModel;
using IdentityServer4.Models;
using IdentityServer4.Services;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Logging;
using VCAuthn.Services.Contracts;
using VCAuthn.Utils;

namespace VCAuthn.Services
{
    public class TokenIssuerService : ITokenIssuerService
    {
        private readonly ITokenCreationService _tokenCreation;
        private readonly ISystemClock _clock;
        private readonly ILogger<TokenIssuerService> _logger;

        public TokenIssuerService(ITokenCreationService tokenCreation, ISystemClock clock, ILogger<TokenIssuerService> logger)
        {
            _tokenCreation = tokenCreation;
            _clock = clock;
            _logger = logger;
        }

        public async Task<string> IssueJwtAsync(int lifetime, string issuer, ICollection<string> audiences, List<Claim> claims)
        {
            _logger.LogDebug($"Issuing token for audience : {audiences.ToJson()}, with claims {claims.ToJson()}, from issuer {issuer}, for lifetime {lifetime}");

            var token = new Token
            {
                CreationTime = _clock.UtcNow.UtcDateTime,
                Issuer = issuer,
                Audiences = audiences,
                Lifetime = lifetime,
                Claims = new HashSet<Claim>(claims, new ClaimComparer())
            };

            return await _tokenCreation.CreateTokenAsync(token);
        }
    }
}