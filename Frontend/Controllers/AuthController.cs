using Microsoft.AspNetCore.Mvc;
using WatchMyExams.Models;
using System.Collections.Generic;
using System.Linq;

namespace WatchMyExams.Controllers
{
    public class AuthController : Controller
    {
        // Temporary user storage
        public static List<User> users = new List<User>();

        public IActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Login(string email, string password)
        {
            var user = users.FirstOrDefault(u => u.Email == email && u.Password == password);

            if (user != null)
            {
                return RedirectToAction("Index", "Dashboard");
            }

            ViewBag.Error = "Invalid Email or Password";
            return View();
        }

        public IActionResult Register()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Register(string name, string email, string password, string role)
        {
            users.Add(new User
            {
                Name = name,
                Email = email,
                Password = password,
                Role = role
            });

            TempData["Success"] = "Account created successfully!";
            return RedirectToAction("Login");
        }

        public IActionResult Logout()
        {
            return RedirectToAction("Login");
        }
    }
}