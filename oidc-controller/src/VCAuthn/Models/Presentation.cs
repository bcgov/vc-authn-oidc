using Newtonsoft.Json;

namespace VCAuthn.Models
{
    public class Presentation
    {
        [JsonProperty("requested_proof")]
        public RequestedProof RequestedProof { get; set; }
    }
}
