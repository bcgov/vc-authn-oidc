using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace VCAuthn.PresentationConfiguration
{
    public interface IPresentationConfigurationService
    {
        Task<PresentationRecord> Find(string presentationConfigId);
    }

    public class PresentationConfigurationService : IPresentationConfigurationService
    {
        public async Task<PresentationRecord> Find(string presentationConfigId)
        {
            return new PresentationRecord
            {
                Id = "tmp",
                SubjectIdentifier = "attribute1",
                Configuration = new PresentationConfiguration()
                {
                    Name = "new configuration"
                }
            };
        }
    }
}