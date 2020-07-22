using Newtonsoft.Json;
using System.Collections.Generic;

namespace VCAuthn.Models
{
    public class RequestedPredicate
    {
        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("label"), Optional]
        public string Label { get; set; }

        [JsonProperty("restrictions")]
        public List<AttributeFilter> Restrictions { get; set; }

        [JsonProperty("p_value")]
        public string PValue { get; set; }

        [JsonProperty("p_type")]
        public string PType { get; set; }
    }
}
