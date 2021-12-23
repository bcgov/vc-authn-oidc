using Newtonsoft.Json;
using System.Collections.Generic;

namespace VCAuthn.Models
{
    public class PresentationRequest
    {
        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("names")]
        public string[] Names { get; set; }

        [JsonProperty("version")]
        public string Version { get; set; }

        [JsonProperty("nonce")]
        public string Nonce { get; set; }

        [JsonProperty("requested_attributes")]
        public Dictionary<string, PresentationAttributeInfo> RequestedAttributes { get; set; }

        [JsonProperty("requested_predicates", NullValueHandling = NullValueHandling.Ignore)]
        public Dictionary<string, PresentationPredicateInfo> RequestedPredicates { get; set; } =
            new Dictionary<string, PresentationPredicateInfo>();

        [JsonProperty("non_revoked", NullValueHandling = NullValueHandling.Ignore)]
        public RevocationInterval NonRevoked { get; set; }

        public override string ToString() =>
            $"{GetType().Name}: " +
            $"Name={Name}, " +
            $"Version={Version}, " +
            $"Nonce={Nonce}, " +
            $"RequestedAttributes={string.Join(",", RequestedAttributes ?? new Dictionary<string, PresentationAttributeInfo>())}, " +
            $"RequestedPredicates={string.Join(",", RequestedPredicates ?? new Dictionary<string, PresentationPredicateInfo>())}, " +
            $"NonRevoked={NonRevoked}";
    }

    /**
      * See https://github.com/hyperledger/aries-rfcs/tree/main/features/0037-present-proof#request-presentation
      * for RFC spec.
      */ 
    class PresentationRequest_v_1_0
    {
        [JsonProperty("name")]
        public string Name { get; set; }
        
        [JsonProperty("version")]
        public string Version { get; set; }

        [JsonProperty("non_revoked", NullValueHandling = NullValueHandling.Ignore)]
        public RevocationInterval NonRevoked { get; set; }

        [JsonProperty("requested_attributes")]
        public Dictionary<string, RequestedAttribute> RequestedAttributes { get; set; } = new Dictionary<string, RequestedAttribute>();

        [JsonProperty("requested_predicates")]
        public Dictionary<string, RequestedPredicate> RequestedPredicates { get; set; } = new Dictionary<string, RequestedPredicate>();
    }
}
