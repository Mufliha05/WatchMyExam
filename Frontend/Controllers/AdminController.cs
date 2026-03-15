using Microsoft.AspNetCore.Mvc;

namespace WatchMyExams.Controllers
{
    public class AdminController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }

        public IActionResult Evidence()
        {
            return View();
        }

        public IActionResult EmailAlerts()
        {
            return View();
        }
    }
}