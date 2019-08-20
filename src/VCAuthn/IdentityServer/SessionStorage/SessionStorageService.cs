using System;
using System.Threading.Tasks;
using Microsoft.Extensions.Options;
using VCAuthn.UrlShortener;

namespace VCAuthn.IdentityServer.SessionStorage
{
    public class SessionStorageServiceOptions
    {
        public int SessionLifetimeInSeconds { get; set; }
    }

    public class SessionStorageService : ISessionStorageService
    {
        private readonly StorageDbContext _context;
        private readonly SessionStorageServiceOptions _options;

        public SessionStorageService(StorageDbContext context, IOptions<SessionStorageServiceOptions> options)
        {
            _context = context;
            _options = options.Value;
        }

        public async Task<string> CreateSessionAsync(string presentationRequestId)
        {
            var session = new AuthSession
            {
                Id = Guid.NewGuid().ToString(),
                PresentationRequestId = presentationRequestId,
                ExpiredTimestamp = DateTime.Now.AddSeconds(_options.SessionLifetimeInSeconds)
            };
            
            if (await AddSession(session))
                return session.Id;

            return null;
        }

        public async Task<bool> AddSession(AuthSession session)
        {
            _context.Add(session);
            return await _context.SaveChangesAsync() == 1;
        }
    }
}