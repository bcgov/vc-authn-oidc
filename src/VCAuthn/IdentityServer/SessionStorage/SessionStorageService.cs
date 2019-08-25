using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;

namespace VCAuthn.IdentityServer.SessionStorage
{
    public class SessionStorageServiceOptions
    {
        public int SessionLifetimeInSeconds { get; set; }
    }

    public class SessionStorageService : ISessionStorageService
    {
        private readonly StorageDbContext _context;
        private readonly ILogger<SessionStorageService> _logger;
        private readonly SessionStorageServiceOptions _options;

        public SessionStorageService(StorageDbContext context, IOptions<SessionStorageServiceOptions> options, ILogger<SessionStorageService> logger)
        {
            _context = context;
            _logger = logger;
            _options = options.Value;
        }

        public async Task<string> CreateSessionAsync(string presentationRequestId)
        {
            var session = new AuthSession
            {
                Id = Guid.NewGuid().ToString(),
                PresentationRequestId = presentationRequestId,
                ExpiredTimestamp = DateTime.UtcNow.AddSeconds(_options.SessionLifetimeInSeconds)
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
        
        public async Task<bool> SatisfyPresentationRequestIdAsync(string presentationRequestId)
        {
            var session = await _context.Sessions.FirstOrDefaultAsync(x => x.PresentationRequestId == presentationRequestId);

            if (session == null)
            {
                _logger.LogWarning($"Couldn't find a corresponding auth session to satisfy. Presentation request id: [{presentationRequestId}]");
                return false;
            }

            session.PresentationRequestSatisfied = true;

            _context.Sessions.Update(session);
            return await _context.SaveChangesAsync() == 1;
        }
        
        public async Task<AuthSession> FindByPresentationIdAsync(string presentationRequestId)
        {
            return await _context.Sessions.FirstOrDefaultAsync(x => x.PresentationRequestId == presentationRequestId);
        }
    }
}