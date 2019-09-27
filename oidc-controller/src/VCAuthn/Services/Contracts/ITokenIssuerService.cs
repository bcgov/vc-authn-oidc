using System.Collections.Generic;
using System.Security.Claims;
using System.Threading.Tasks;

namespace VCAuthn.Services.Contracts
{
    /// <summary>
    /// A token issuer service.
    /// </summary>
    public interface ITokenIssuerService
    {
        /// <summary>
        /// Issues a JWT.
        /// </summary>
        Task<string> IssueJwtAsync(int lifetime, string issuer, ICollection<string> audiences, List<Claim> claims);
    }
}