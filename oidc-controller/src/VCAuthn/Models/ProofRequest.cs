using System.Collections.Generic;
using Newtonsoft.Json;

namespace VCAuthn.Models
{
    class ProofRequest_v_1_0
    {
        [JsonProperty("name")]
        public string Name { get; set; }
        
        [JsonProperty("version")]
        public string Version { get; set; }

        [JsonProperty("requested_attributes")]
        public Dictionary<string, RequestedAttribute> RequestedAttributes { get; set; } = new Dictionary<string, RequestedAttribute>();

        [JsonProperty("requested_predicates")]
        public Dictionary<string, RequestedPredicate> RequestedPredicates { get; set; } = new Dictionary<string, RequestedPredicate>();
    }
}

