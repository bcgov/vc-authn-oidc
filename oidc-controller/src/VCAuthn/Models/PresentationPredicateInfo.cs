using Newtonsoft.Json;

namespace VCAuthn.Models
{
    /// <inheritdoc />
    public class PresentationPredicateInfo : PresentationAttributeInfo
    {
        [JsonProperty("p_type")]
        public string PredicateType { get; set; }

        [JsonProperty("p_value")]
        public string PredicateValue { get; set; }

        public override string ToString() =>
            $"{GetType().Name}: " +
            $"PredicateType={PredicateType}, " +
            $"PredicateValue={PredicateValue}";
    }
}
