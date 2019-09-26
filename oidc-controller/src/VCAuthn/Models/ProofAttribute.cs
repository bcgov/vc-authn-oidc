using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;

namespace VCAuthn.Models
{
    public class ProofAttribute
    {
        [JsonProperty("raw")]
        public string Raw { get; set; }

        /// <summary>
        /// ignore structural mapping of other properties
        /// </summary>
        [JsonExtensionData]
        public IDictionary<string, JToken> Rest { get; set; }
    }
}
