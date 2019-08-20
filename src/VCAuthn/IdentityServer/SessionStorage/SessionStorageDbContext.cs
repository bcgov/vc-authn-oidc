using Microsoft.EntityFrameworkCore;
using VCAuthn.UrlShortener;

namespace VCAuthn.IdentityServer.SessionStorage
{
    public class SessionStorageDbContext : DbContext
    {
        public SessionStorageDbContext(DbContextOptions<SessionStorageDbContext> options) : base(options) { }

        public DbSet<AuthSession> Sessions { get; set; }
    }
}