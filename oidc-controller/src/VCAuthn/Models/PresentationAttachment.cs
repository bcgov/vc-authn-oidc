using System.Collections.Generic;
using Newtonsoft.Json;

namespace VCAuthn.Models
{
    public class PresentationAttachment
    {
        [JsonProperty("@id")]
        public string Id { get; set; }

        [JsonProperty("mime-type")]
        public string MimeType { get; set; }

        [JsonProperty("data")]
        public Dictionary<string, string> Data { get; set; }
    }
}