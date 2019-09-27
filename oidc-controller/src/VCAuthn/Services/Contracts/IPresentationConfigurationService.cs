using System.Collections.Generic;
using System.Threading.Tasks;

namespace VCAuthn.Services.Contracts
{
    public interface IPresentationConfigurationService
    {
        void Create(Models.PresentationConfiguration record);
        Task CreateAsync(Models.PresentationConfiguration record);
        bool Exists(string id);
        Task<bool> ExistsAsync(string id);
        Models.PresentationConfiguration Get(string id);
        Task<Models.PresentationConfiguration> GetAsync(string id);
        List<Models.PresentationConfiguration> GetAll();
        Task<List<Models.PresentationConfiguration>> GetAllAsync();
        void Update(Models.PresentationConfiguration record);
        Task UpdateAsync(Models.PresentationConfiguration record);
        bool Delete(string id);
        Task<bool> DeleteAsync(string id);
    }
}
