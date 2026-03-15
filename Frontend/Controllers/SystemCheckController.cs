using Microsoft.AspNetCore.Mvc;

namespace WatchMyExams.Controllers
{
    public class SystemCheckController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}