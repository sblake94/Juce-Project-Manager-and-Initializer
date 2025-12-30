using Microsoft.AspNetCore.Mvc;

namespace ProjectManager.Backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ProjectApiController : ControllerBase
    {
        [HttpPost(nameof(Handshake))]
        public IActionResult Handshake()
        {
            //return NotFound(); 
            return Ok("Handshake successful");
        }
    }
}
