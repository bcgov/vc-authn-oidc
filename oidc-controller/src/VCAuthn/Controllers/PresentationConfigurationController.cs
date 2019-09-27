using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using VCAuthn.Models;
using VCAuthn.Services.Contracts;

namespace VCAuthn.Controllers
{
    [Route("api/vc-configs")]
    [ApiController]
    [Authorize]
    public class PresentationConfigurationController : ControllerBase
    {
        private readonly IPresentationConfigurationService _service;

        public PresentationConfigurationController(IPresentationConfigurationService service)
        {
            _service = service;
        }

        // GET: api/vc-configs
        [HttpGet]
        public async Task<ActionResult<PresentationConfiguration>> GetConfigs()
        {
            return Ok(await _service.GetAllAsync());
        }

        // GET: api/vc-configs/5
        [HttpGet("{id}")]
        public async Task<ActionResult<PresentationConfiguration>> GetConfig(string id)
        {
            var record = await _service.GetAsync(id);

            if (record == null)
            {
                return NotFound();
            }

            return Ok(record);
        }
        
        // POST: api/vc-configs
        [HttpPost]
        public async Task<ActionResult> CreateConfig([FromBody] PresentationConfiguration record)
        {
            if (_service.Exists(record.Id))
                return BadRequest($"Record with id : `{record.Id}` already exists");

            await _service.CreateAsync(record);
            return CreatedAtAction(nameof(GetConfig), new { id = record.Id }, record);
        }
        
        // PUT: api/vc-configs
        [HttpPut]
        public async Task<ActionResult> UpdateConfig([FromBody] PresentationConfiguration record)
        {
            await _service.UpdateAsync(record);
            return Ok();
        }
        
        // DELETE: api/vc-configs/5
        [HttpDelete("{id}")]
        public async Task<ActionResult> DeleteConfig(string id)
        {
            await _service.DeleteAsync(id);
            return Ok();
        }
    }
}