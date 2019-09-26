using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;

namespace VCAuthn.Models
{
    public class RequestedProof
    {
        [JsonProperty("revealed_attrs")]
        public Dictionary<string, ProofAttribute> RevealedAttributes { get; set; }

        /// <summary>
        /// ignore structural mapping of other properties
        /// </summary>
        [JsonExtensionData]
        public IDictionary<string, JToken> Rest { get; set; }
    }
}
