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
                .Property<string>("Config")
                .HasColumnName("_configuration");

            modelBuilder.Entity<AuthSession>()
                .Property<string>("Proof")
                .HasColumnName("_presentation");

            modelBuilder.Entity<AuthSession>()
                .Property<string>("RequestParams")
                .HasColumnName("_requestParameters");
        }

    }
}