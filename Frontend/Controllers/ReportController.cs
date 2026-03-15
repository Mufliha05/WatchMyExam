using Microsoft.AspNetCore.Mvc;

namespace WatchMyExams.Controllers
{
    public class ReportController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
