using Microsoft.AspNetCore.Mvc;

namespace WatchMyExams.Controllers
{
    public class SettingsController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
