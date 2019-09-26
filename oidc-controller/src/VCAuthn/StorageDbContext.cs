using Microsoft.EntityFrameworkCore;
using VCAuthn.IdentityServer.SessionStorage;
using VCAuthn.PresentationConfiguration;
using VCAuthn.UrlShortener;

namespace VCAuthn
{
    public class StorageDbContext : DbContext
    {
        public StorageDbContext(DbContextOptions<StorageDbContext> options) : base(options) { }

        public DbSet<AuthSession> Sessions { get; set; }
        public DbSet<PresentationRecord> PresentationConfigurations { get; set; }
        public DbSet<MappedUrl> MappedUrls { get; set; }
        
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<PresentationRecord>()
                .Property<string>("Config")
                .HasField("_configuration");
            
            modelBuilder.Entity<AuthSession>()
                .Property<string>("Proof")
                .HasField("_presentation");

            modelBuilder.Entity<AuthSession>()
                .Property<string>("RequestParams")
                .HasField("_requestParameters");

            modelBuilder.Entity<AuthSession>()
                .Property<string>("ProofRequest")
                .HasField("_presentationRequest");
        }

    }
}