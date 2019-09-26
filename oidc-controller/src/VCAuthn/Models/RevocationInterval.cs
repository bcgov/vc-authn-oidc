using Newtonsoft.Json;

namespace VCAuthn.Models
{
    public class RevocationInterval
    {
        [JsonProperty("from")]
        public uint From { get; set; }

        [JsonProperty("to")]
        public uint To { get; set; }

        public override string ToString() =>
            $"{GetType().Name}: " +
            $"From={From}, " +
            $"To={To}";
    }
}
