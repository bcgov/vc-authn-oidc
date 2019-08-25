using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using VCAuthn.IdentityServer;
using VCAuthn.IdentityServer.SessionStorage;

namespace VCAuthn.Controllers
{
    public class PresentationRequestController : ControllerBase
    {
        private readonly ISessionStorageService _sessionStorageService;
        private readonly ILogger<WebHooksController> _logger;

        public PresentationRequestController(ISessionStorageService sessionStorageService, ILogger<WebHooksController> logger)
        {
            _sessionStorageService = sessionStorageService;
            _logger = logger;
        }

        [HttpPost(IdentityConstants.VerificationChallengePollUri)]
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
                return BadRequest();
            
            if (authSession.ExpiredTimestamp >= DateTime.UtcNow)
            {
                _logger.LogDebug($"Session expired. Session id: [{authSession.Id}]");
                return BadRequest();
            }

            return Ok();
        }
    }
}