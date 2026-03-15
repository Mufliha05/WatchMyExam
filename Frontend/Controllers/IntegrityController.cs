using Microsoft.AspNetCore.Mvc;

namespace WatchMyExams.Controllers
{
    public class IntegrityController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}