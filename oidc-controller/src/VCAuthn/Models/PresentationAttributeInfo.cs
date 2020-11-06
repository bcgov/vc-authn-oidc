using Newtonsoft.Json;
using System.Collections.Generic;

namespace VCAuthn.Models
{
    public class PresentationAttributeInfo
    {
        [JsonProperty("name", NullValueHandling = NullValueHandling.Ignore)]
        public string Name { get; set; }

        [JsonProperty("names", NullValueHandling = NullValueHandling.Ignore)]
        public string[] Names { get; set; }

        /// <summary>
        /// Gets or sets the restrictions.
        /// <code>
        /// filter_json: filter for credentials
        ///    {
        ///        "schema_id": string, (Optional)
        ///        "schema_issuer_did": string, (Optional)
        ///        "schema_name": string, (Optional)
        ///        "schema_version": string, (Optional)
        ///        "issuer_did": string, (Optional)
        ///        "cred_def_id": string, (Optional)
        ///    }
        /// </code>
        /// </summary>
        /// <value>The restrictions.</value>
        [JsonProperty("restrictions", NullValueHandling = NullValueHandling.Ignore)]
        public List<AttributeFilter> Restrictions { get; set; }

        /// <summary>
        /// Gets or sets the non revoked interval.
        /// </summary>
        [JsonProperty("non_revoked", NullValueHandling = NullValueHandling.Ignore)]
        public RevocationInterval NonRevoked { get; set; }

        public override string ToString() =>
            $"{GetType().Name}: " +
            $"Name={Name}, " +
            $"Names={Names}, " +
            $"Restrictions={string.Join(",", Restrictions ?? new List<AttributeFilter>())}, " +
            $"NonRevoked={NonRevoked}";
    }
}
