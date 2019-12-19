using System.Collections.Generic;
using Newtonsoft.Json;

namespace VCAuthn.Models
{
    public class PresentationRequestMessage
    {
        [JsonProperty("@id")]
        public string Id { get; set; }

        [JsonProperty("@type")]
        public string Type => "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation";

        [JsonProperty("request_presentations~attach")]
        public List<PresentationAttachment> Request { get; set; }

        [JsonProperty("comment")]
        public string Comment { get; set; }

        [JsonProperty("~service")]
        public ServiceDecorator Service { get; set; }
    }

    public class ServiceDecorator
    {
        [JsonProperty("recipientKeys")]
        public List<string> RecipientKeys { get; set; }

        [JsonProperty("routingKeys")]
        public List<string> RoutingKeys { get; set; }

        [JsonProperty("serviceEndpoint")]
        public string ServiceEndpoint { get; set; }
    }
}