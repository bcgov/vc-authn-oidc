using System.Collections.Generic;
using Newtonsoft.Json;

namespace VCAuthn.IdentityServer.Endpoints
{
    public class PresentationRequest
    {
        [JsonProperty("@id")]
        public string Id { get; set; }

        [JsonProperty("@type")]
        public string Type => "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-presentation/0.1/presentation-request";

        [JsonProperty("request")]
        public PresentationConfiguration.PresentationConfiguration Request { get; set; }
        
        [JsonProperty("comment")]
        public string Comment { get; set; }
        
        [JsonProperty("thread_id")]
        public string ThreadId { get; set; }
        
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