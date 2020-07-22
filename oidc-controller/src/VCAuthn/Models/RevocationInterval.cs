using Newtonsoft.Json;

namespace VCAuthn.Models
{
    public class RevocationInterval
    {
        [JsonProperty("from")]
        public long From { get; set; }

        [JsonProperty("to")]
        public long To { get; set; }

        public override string ToString() =>
            $"{GetType().Name}: " +
            $"From={From}, " +
            $"To={To}";
    }
}
