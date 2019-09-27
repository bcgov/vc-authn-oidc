using System;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using VCAuthn.Migrations;
using VCAuthn.Models;
using VCAuthn.Services.Contracts;

namespace VCAuthn.Services
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

        public async Task<AuthSession> CreateSessionAsync(AuthSession session)
        {
            session.Id = Guid.NewGuid().ToString();
            session.ExpiredTimestamp = DateTime.UtcNow.AddSeconds(_options.SessionLifetimeInSeconds);

            if (await AddSession(session))
                return session;

            return null;
        }

        public async Task<bool> AddSession(AuthSession session)
        {
            _context.Add(session);
            return await _context.SaveChangesAsync() == 1;
        }

        public async Task<bool> SatisfyPresentationRequestIdAsync(string presentationRequestId, Presentation partialPresentation)
        {
            var session = await _context.Sessions.FirstOrDefaultAsync(x => x.PresentationRequestId == presentationRequestId);

            if (session == null)
            {
                _logger.LogWarning($"Couldn't find a corresponding auth session to satisfy. Presentation request id: [{presentationRequestId}]");
                return false;
            }

            session.PresentationRequestSatisfied = true;
            session.Presentation = partialPresentation;

            _context.Sessions.Update(session);
            return await _context.SaveChangesAsync() == 1;
        }

        public async Task<AuthSession> FindByPresentationIdAsync(string presentationRequestId)
        {
            return await _context.Sessions.FirstOrDefaultAsync(x => x.PresentationRequestId == presentationRequestId);
        }

        public async Task<AuthSession> FindBySessionIdAsync(string sessionId)
        {
            return await _context.Sessions.FirstOrDefaultAsync(x => x.Id == sessionId);
        }

        public bool DeleteSession(AuthSession session)
        {
            if (session == null)
                return false;

            _context.Sessions.Remove(session);
            return _context.SaveChanges() == 1;
        }
    }
}