using System;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using VCAuthn.ACAPY;
using VCAuthn.IdentityServer.SessionStorage;

namespace VCAuthn.Controllers
{
    [Route("/topic")]
    public class WebHooksController : ControllerBase
    {
        private readonly ISessionStorageService _sessionStorageService;
        private readonly ILogger<WebHooksController> _logger;

        public WebHooksController(ISessionStorageService sessionStorageService, ILogger<WebHooksController> logger)
        {
            _sessionStorageService = sessionStorageService;
            _logger = logger;
        }
        
        
        [HttpPost("{topic}")]
        public async Task<ActionResult> GetTopicUpdate(string topic)
        {
            if (String.Equals(ACAPYConstants.PresentationsTopic, topic, StringComparison.InvariantCultureIgnoreCase) == false)
            {
                _logger.LogDebug($"Skipping webhook for topic [{topic}]");
                return Ok();
            }
            
            string payload;
            using (var reader = new StreamReader(Request.Body, Encoding.UTF8))
            {  
                payload = await reader.ReadToEndAsync();
            }
            _logger.LogInformation($"Topic [{topic}], Payload [{payload}]");

            try
            {
                var update = JsonConvert.DeserializeObject<PresentationUpdate>(payload);

                if (update.State != ACAPYConstants.SuccessfulPresentationUpdate)
                {
                    return Ok();
                }
                
                var proof = update.Presentation["requested_proof"].ToObject<RequestedProof>();
                var partialPresentation = new PartialPresentation
                {
                    RequestedProof = proof
                };
                
                await _sessionStorageService.SatisfyPresentationRequestIdAsync(update.ThreadId, partialPresentation);
            }
            catch (Exception e)
            {
                _logger.LogError(e, "Failed to deserialize a payload");
            }

            return Ok();
        }

        public class PresentationUpdate
        {
            [JsonProperty("created_at")]
            public DateTime CreatedAt { get; set; }

            [JsonProperty("initiator")]
            public string Initiator { get; set; }

            [JsonProperty("presentation_exchange_id")]
            public string PresentationExchangeId { get; set; }

            [JsonProperty("updated_at")]
            public DateTime UpdatedAt { get; set; }

            [JsonProperty("connection_id")]
            public string ConnectionId { get; set; }

            [JsonProperty("state")]
            public string State { get; set; }
            
            [JsonProperty("thread_id")]
            public string ThreadId { get; set; }

            [JsonProperty("presentation_request")]
            public JObject PresentationRequest { get; set; }

            [JsonProperty("presentation")]
            public JObject Presentation { get; set; }
        }
    }
}