using Microsoft.EntityFrameworkCore;
using VCAuthn.Models;

namespace VCAuthn.Migrations
{
    public class StorageDbContext : DbContext
    {
        public StorageDbContext(DbContextOptions<StorageDbContext> options) : base(options) { }
        public DbSet<AuthSession> Sessions { get; set; }
        public DbSet<PresentationConfiguration> PresentationConfigurations { get; set; }
        public DbSet<MappedUrl> MappedUrls { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<PresentationConfiguration>()
                .Property<string>("_configuration")
                .HasColumnName("Config");

            modelBuilder.Entity<AuthSession>()
                .Property<string>("_presentation")
                .HasColumnName("Proof");

            modelBuilder.Entity<AuthSession>()
                .Property<string>("_requestParameters")
                .HasColumnName("RequestParams");
            
            modelBuilder.Entity<AuthSession>()
                .Property<string>("_presentationRequest")
                .HasColumnName("ProofRequest");
        }

    }
}