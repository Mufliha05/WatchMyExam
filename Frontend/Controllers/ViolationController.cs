using Microsoft.AspNetCore.Mvc;

namespace WatchMyExams.Controllers
{
    public class ViolationController : Controller
    {

        [HttpPost]
        public IActionResult SaveViolation(string type)
        {
            Console.WriteLine("Violation Detected: " + type);

            return Json(new { success = true });
        }

    }
}