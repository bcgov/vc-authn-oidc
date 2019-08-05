using Microsoft.AspNetCore.Mvc;

namespace VCAuthn.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
