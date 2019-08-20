using Microsoft.EntityFrameworkCore;

namespace VCAuthn.UrlShortener
{
    public class UrlShortenerServiceDbContext : DbContext
    {
        public UrlShortenerServiceDbContext(DbContextOptions<UrlShortenerServiceDbContext> options) : base(options) { }

        public DbSet<MappedUrl> MappedUrls { get; set; }
    }
}