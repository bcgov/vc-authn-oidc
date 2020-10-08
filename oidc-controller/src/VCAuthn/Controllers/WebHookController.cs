using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using VCAuthn.ACAPY;
using VCAuthn.Models;
using VCAuthn.Services.Contracts;
using VCAuthn.Utils;

namespace VCAuthn.Controllers
{
    [ApiExplorerSettings(IgnoreApi = true)]
    public class WebHooksController : ControllerBase
    {
        private readonly ISessionStorageService _sessionStorageService;
        private readonly IConfiguration _config;
        private static Serilog.ILogger Log => Serilog.Log.ForContext<WebHooksController>();

        public WebHooksController(ISessionStorageService sessionStorageService, IConfiguration config)
        {
            _sessionStorageService = sessionStorageService;
            _config = config;
        }


        [HttpPost("/{apiKey}/topic/{topic}")]
        public Task<ActionResult> GetTopicUpdateWithApiKey([FromRoute] string apiKey, [FromRoute] string topic, [FromBody] PresentationUpdate update)
        {
            return ProcessWebhook(apiKey, topic, update);
        }

        [HttpPost("/topic/{topic}")]
        public Task<ActionResult> GetTopicUpdate([FromRoute] string topic, [FromBody] PresentationUpdate update)
        {
            return ProcessWebhook(null, topic, update);
        }

        private async Task<ActionResult> ProcessWebhook(string apiKey, string topic, PresentationUpdate update)
        {
            if (!string.IsNullOrEmpty(_config.GetValue<string>("ApiKey")) && !string.Equals(_config.GetValue<string>("ApiKey"), apiKey))
            {
                Log.Debug($"Web hook operation un-authorized");
                return Unauthorized();
            }

            if (string.Equals(ACAPYConstants.PresentationsTopic, topic, StringComparison.InvariantCultureIgnoreCase) == false)
            {
                Log.Debug($"Skipping webhook for topic [{topic}]");
                return Ok();
            }

            Log.Debug($"Received web hook update object : {update.ToJson()}");

            try
            {
                if (update.State != ACAPYConstants.SuccessfulPresentationUpdate)
                {
                    Log.Debug($"Presentation Request not yet received, state is [{update.State}]");
                    return Ok();
                }

                var proof = update.Presentation["requested_proof"].ToObject<RequestedProof>();
                var partialPresentation = new Presentation
                {
                    RequestedProof = proof
                };

                Log.Debug($"Marking Presentation Request with id : {update.PresentationExchangeId} as satisfied");

                await _sessionStorageService.SatisfyPresentationRequestIdAsync(update.PresentationExchangeId, partialPresentation);
            }
            catch (Exception e)
            {
                Log.Error(e, "Failed to deserialize a payload");
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

            [JsonProperty("verified")]
            public Boolean Verified { get; set; }
        }
    }
}