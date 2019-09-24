using System.Threading.Tasks;

namespace VCAuthn.PresentationConfiguration
{
    public interface IPresentationConfigurationService
    {
        void Create(PresentationRecord record);
        Task CreateAsync(PresentationRecord record);
        bool Exists(string id);
        Task<bool> ExistsAsync(string id);
        PresentationRecord Get(string id);
        Task<PresentationRecord> GetAsync(string id);
        void Update(PresentationRecord record);
        Task UpdateAsync(PresentationRecord record);
        bool Delete(string id);
        Task<bool> DeleteAsync(string id);
    }

    public class PresentationConfigurationService : IPresentationConfigurationService
    {
        private readonly StorageDbContext _context;

        public PresentationConfigurationService(StorageDbContext context)
        {
            _context = context;
        }
        
        public void Create(PresentationRecord record)
        {
            _context.Add(record);
            _context.SaveChanges();
        }

        public async Task CreateAsync(PresentationRecord record)
        {
            await _context.AddAsync(record);
            await _context.SaveChangesAsync();
        }
        
        public PresentationRecord Get(string id)
        {
            return _context.PresentationConfigurations.Find(id);
        }
        
        public async Task<PresentationRecord> GetAsync(string id)
        {
            return await _context.PresentationConfigurations.FindAsync(id);
        }

        public bool Exists(string id)
        {
            return (_context.PresentationConfigurations.Find(id) != null);
        }

        public async Task<bool> ExistsAsync(string id)
        {
            return (await _context.PresentationConfigurations.FindAsync(id) != null);
        }

        public void Update(PresentationRecord record)
        {
            var original = _context.PresentationConfigurations.Find(record.Id);

            if (original == null)
            {
                return;
            }

            original.Configuration = record.Configuration;
            original.SubjectIdentifier = record.SubjectIdentifier;
            
            _context.Update(original);
            _context.SaveChanges();
        }

        public async Task UpdateAsync(PresentationRecord record)
        {
            var original = await _context.PresentationConfigurations.FindAsync(record.Id);

            if (original == null)
            {
                return;
            }

            original.Configuration = record.Configuration;
            original.SubjectIdentifier = record.SubjectIdentifier;
            
            _context.Update(original);
            await _context.SaveChangesAsync();
        }
        
        public bool Delete(string id)
        {
            var record = _context.PresentationConfigurations.Find(id);

            if (record == null)
            {
                return false;
            }

            _context.PresentationConfigurations.Remove(record);
            return _context.SaveChanges() == 1;
        }
        
        public async Task<bool> DeleteAsync(string id)
        {
            var record = await _context.PresentationConfigurations.FindAsync(id);

            if (record == null)
            {
                return false;
            }

            _context.PresentationConfigurations.Remove(record);
            return _context.SaveChanges() == 1;
        }
    }
}