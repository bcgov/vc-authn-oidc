using Newtonsoft.Json;
using System.Collections.Generic;

namespace VCAuthn.Models
{
    public class PresentationRequestConfiguration
    {
        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("version")]
        public string Version { get; set; }

        [JsonProperty("requested_attributes")]
        public List<RequestedAttribute> RequestedAttributes { get; set; } = new List<RequestedAttribute>();

        [JsonProperty("requested_predicates")]
        public List<RequestedPredicate> RequestedPredicates { get; set; } = new List<RequestedPredicate>();
    }
}
