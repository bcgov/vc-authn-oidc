using Newtonsoft.Json;
using System.Collections.Generic;

namespace VCAuthn.Models
{
    public class RequestedAttribute
    {
        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("names")]
        public string[] Names { get; set; }

        [JsonProperty("label"), Optional]
        public string Label { get; set; }

        [JsonProperty("restrictions")]
        public List<AttributeFilter> Restrictions { get; set; }
    }
}
