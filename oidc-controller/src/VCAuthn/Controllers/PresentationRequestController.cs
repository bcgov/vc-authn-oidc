using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using VCAuthn.IdentityServer;
using VCAuthn.Services.Contracts;

namespace VCAuthn.Controllers
{
    [ApiExplorerSettings(IgnoreApi = true)]
    public class PresentationRequestController : ControllerBase
    {
        private readonly ISessionStorageService _sessionStorageService;
        private readonly IUrlShortenerService _urlShortenerService;
        private static Serilog.ILogger Log => Serilog.Log.ForContext<PresentationRequestController>();

        public PresentationRequestController(ISessionStorageService sessionStorageService, IUrlShortenerService urlShortenerService)
        {
            _sessionStorageService = sessionStorageService;
            _urlShortenerService = urlShortenerService;
        }

        [HttpGet(IdentityConstants.ChallengePollUri)]
        public async Task<ActionResult> Poll([FromQuery(Name = IdentityConstants.ChallengeIdQueryParameterName)] string presentationRequestId)
        {
            if (string.IsNullOrEmpty(presentationRequestId))
            {
                Log.Debug($"Missing presentation request Id");
                return NotFound();
            }

            var authSession = await _sessionStorageService.FindByPresentationIdAsync(presentationRequestId);
            if (authSession == null)
            {
                Log.Debug($"Cannot find a session corresponding to the presentation request. Presentation request Id: [{presentationRequestId}]");
                return NotFound();
            }

            if (authSession.PresentationRequestSatisfied == false)
            {
                Log.Debug($"Presentation request was not satisfied. AuthSession: [{authSession}]");
                return BadRequest();
            }


            return Ok();
        }

        [HttpGet("/url/{key}")]
        public async Task<ActionResult> ResolveUrl(string key)
        {
            Log.Debug($"Resolving shortened url: {Request.Path.Value}");

            if (string.IsNullOrEmpty(key))
            {
                Log.Debug("Url key is null or empty");
                return BadRequest();
            }

            var url = await _urlShortenerService.GetUrlAsync(key);
            if (string.IsNullOrEmpty(url))
            {
                Log.Debug($"Url is empty. Url key: [{key}]");
                return NotFound();
            }
            
            Log.Debug($"Redirecting to {url}");
            return Redirect(url);
        }
    }
}