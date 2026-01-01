using Microsoft.AspNetCore.Mvc;

namespace ProjectManager.Backend.Controllers.Extensions
{
    public static class ControllerBaseExtensions
    {
        public static IActionResult NotImplemented(this ControllerBase controller)
        {
            return controller.StatusCode(501, "This feature is not implemented yet.");
        }
    }
}
