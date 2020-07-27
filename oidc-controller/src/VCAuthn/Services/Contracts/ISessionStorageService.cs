using System.Threading.Tasks;
using VCAuthn.Models;

namespace VCAuthn.Services.Contracts
{
    public interface ISessionStorageService
    {
        Task<AuthSession> CreateSessionAsync(AuthSession session);
        Task<bool> AddSession(AuthSession session);
        Task<bool> UpdatePresentationRequestIdAsync(string presentationRequestId, Presentation partialPresentation, bool verified = false);
        Task<AuthSession> FindByPresentationIdAsync(string presentationRequestId);
        Task<AuthSession> FindBySessionIdAsync(string sessionId);
        bool DeleteSession(AuthSession session);
    }
}