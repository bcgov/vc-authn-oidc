using System.Threading.Tasks;

namespace VCAuthn.IdentityServer.SessionStorage
{
    public interface ISessionStorageService
    {
        Task<string> CreateSessionAsync(string presentationRequestId);
        Task<bool> AddSession(AuthSession session);
    }
}