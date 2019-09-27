using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using VCAuthn.Migrations;
using VCAuthn.Models;
using VCAuthn.Services.Contracts;

namespace VCAuthn.Services
{
    public class PresentationConfigurationService : IPresentationConfigurationService
    {
        private readonly StorageDbContext _context;

        public PresentationConfigurationService(StorageDbContext context)
        {
            _context = context;
        }
        
        public void Create(PresentationConfiguration record)
        {
            _context.Add(record);
            _context.SaveChanges();
        }

        public async Task CreateAsync(PresentationConfiguration record)
        {
            await _context.AddAsync(record);
            await _context.SaveChangesAsync();
        }
        
        public PresentationConfiguration Get(string id)
        {
            return _context.PresentationConfigurations.Find(id);
        }
        
        public async Task<PresentationConfiguration> GetAsync(string id)
        {
            return await _context.PresentationConfigurations.FindAsync(id);
        }

        public List<PresentationConfiguration> GetAll()
        {
            return _context.PresentationConfigurations.ToList();
        }

        public Task<List<PresentationConfiguration>> GetAllAsync()
        {
            return Task.FromResult(_context.PresentationConfigurations.ToList());
        }

        public bool Exists(string id)
        {
            return (_context.PresentationConfigurations.Find(id) != null);
        }

        public async Task<bool> ExistsAsync(string id)
        {
            return (await _context.PresentationConfigurations.FindAsync(id) != null);
        }

        public void Update(PresentationConfiguration record)
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

        public async Task UpdateAsync(PresentationConfiguration record)
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