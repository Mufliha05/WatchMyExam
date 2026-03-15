using Microsoft.AspNetCore.Mvc;

namespace WatchMyExams.Controllers
{
    public class DashboardController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}