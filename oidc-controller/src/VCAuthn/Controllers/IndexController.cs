using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;

namespace VCAuthn.Controllers
{
    [ApiExplorerSettings(IgnoreApi = true)]
    public class IndexController : Controller
    {
        private readonly IConfiguration _configuration;

        public IndexController(IConfiguration configuration) : base()
        {
            _configuration = configuration;
        }

        [HttpGet]
        [Route("/")]
        [ApiExplorerSettings(IgnoreApi = true)]
        public IActionResult Index()
        {
            if (_configuration.GetValue<bool>("SwaggerEnabled"))
                return Redirect("/swagger");
            return NotFound();
        }
    }
}