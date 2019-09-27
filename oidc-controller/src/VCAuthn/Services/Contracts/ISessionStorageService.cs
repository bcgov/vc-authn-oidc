using System.Threading.Tasks;
using VCAuthn.Models;

namespace VCAuthn.Services.Contracts
{
    public interface ISessionStorageService
    {
        Task<AuthSession> CreateSessionAsync(AuthSession session);
        Task<bool> AddSession(AuthSession session);
        Task<bool> SatisfyPresentationRequestIdAsync(string presentationRequestId, Presentation partialPresentation);
        Task<AuthSession> FindByPresentationIdAsync(string presentationRequestId);
        Task<AuthSession> FindBySessionIdAsync(string sessionId);
        bool DeleteSession(AuthSession session);
    }
}