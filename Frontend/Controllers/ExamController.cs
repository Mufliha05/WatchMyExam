using Microsoft.AspNetCore.Mvc;

namespace WatchMyExams.Controllers
{
    public class ExamController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}