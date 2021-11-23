using System;
using System.Web;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Primitives;
using VCAuthn.IdentityServer;
using VCAuthn.Services.Contracts;
using VCAuthn.Utils;

namespace VCAuthn.Controllers
{
    [ApiExplorerSettings(IgnoreApi = true)]
    public class PresentationRequestController : ControllerBase
    {
        private readonly ISessionStorageService _sessionStorageService;
        private readonly IUrlShortenerService _urlShortenerService;
        private readonly ILogger<WebHooksController> _logger;

        public PresentationRequestController(ISessionStorageService sessionStorageService, IUrlShortenerService urlShortenerService, ILogger<WebHooksController> logger)
        {
            _sessionStorageService = sessionStorageService;
            _urlShortenerService = urlShortenerService;
            _logger = logger;
        }

        [HttpGet(IdentityConstants.ChallengePollUri)]
        public async Task<ActionResult> Poll([FromQuery(Name = IdentityConstants.ChallengeIdQueryParameterName)] string presentationRequestId)
        {
            if (string.IsNullOrEmpty(presentationRequestId))
            {
                _logger.LogDebug($"Missing presentation request Id");
                return NotFound();
            }

            var authSession = await _sessionStorageService.FindByPresentationIdAsync(presentationRequestId);
            if (authSession == null)
            {
                _logger.LogDebug($"Cannot find a session corresponding to the presentation request. Presentation request Id: [{presentationRequestId}]");
                return NotFound();
            }

            if (authSession.PresentationRequestSatisfied == false)
            {
                _logger.LogDebug($"Presentation request was not satisfied. AuthSession: [{authSession}]");
                return BadRequest();
            }


            return Ok();
        }

        [HttpGet("/url/{key}")]
        public async Task<ActionResult> ResolveUrl(string key)
        {
            _logger.LogDebug($"Resolving shortened url: {Request.Path.Value}");

            if (string.IsNullOrEmpty(key))
            {
                _logger.LogDebug("Url key is null or empty");
                return BadRequest();
            }

            var url = await _urlShortenerService.GetUrlAsync(key);
            if (string.IsNullOrEmpty(url))
            {
                _logger.LogDebug($"Url is empty. Url key: [{key}]");
                return NotFound();
            }

            Request.Headers.TryGetValue("Accept", out var accept);
            if (!StringValues.IsNullOrEmpty(accept) && ((ICollection<string>)accept).Contains("application/json"))
            {

                var uri = new Uri(url);
                var message = HttpUtility.ParseQueryString(uri.Query)["m"];
                if (string.IsNullOrEmpty(message)) {
                    _logger.LogDebug("Url query param is null or empty");
                    return StatusCode(StatusCodes.Status500InternalServerError);
                }

                var jsonMessage = message.FromBase64Url();
                if (string.IsNullOrEmpty(jsonMessage)) {
                    _logger.LogDebug("JSON is null or empty");
                    return StatusCode(StatusCodes.Status500InternalServerError);
                }

                _logger.LogDebug($"Returning JSON");
                Response.Headers.Add("Location", url);
                return Content(jsonMessage, "application/json; charset=utf-8");
            }

            _logger.LogDebug($"Redirecting to {url}");
            return Redirect(url);
        }
    }
}