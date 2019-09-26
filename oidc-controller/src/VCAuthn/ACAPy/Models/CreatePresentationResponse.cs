using Newtonsoft.Json;
using VCAuthn.Models;

namespace VCAuthn.ACAPY
{
    public class CreatePresentationResponse
    {
        [JsonProperty("thread_id")]
        public string ThreadId { get; set; }

        [JsonProperty("presentation_exchange_id")]
        public string PresentationExchangeId { get; set; }

        [JsonProperty("presentation_request")]
        public PresentationRequest PresentationRequest { get; set; }
    }
}