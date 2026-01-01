using Microsoft.AspNetCore.Mvc;
using ProjectManager.Backend.Controllers.Extensions;

namespace ProjectManager.Backend.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ComponentController : ControllerBase
{
    /// <summary>
    /// Create a new component.
    /// </summary>
    /// <returns></returns>
    [HttpPost(nameof(Create))]
    public IActionResult Create()
    {
        return this.NotImplemented();
    }

    /// <summary>
    /// Get a component.
    /// </summary>
    /// <returns></returns>
    [HttpGet(nameof(Get))]
    public IActionResult Get()
    {
        return this.NotImplemented();
    }

    /// <summary>
    /// Overwrite a component.
    /// </summary>
    /// <returns></returns>
    [HttpPut(nameof(Put))]
    public IActionResult Put()
    {
        return this.NotImplemented();
    }

    /// <summary>
    /// Partially update a component.
    /// </summary>
    /// <returns></returns>
    [HttpPatch(nameof(Patch))]
    public IActionResult Patch()
    {
        return this.NotImplemented();
    }

    /// <summary>
    /// Delete a component.
    /// </summary>
    /// <returns></returns>
    [HttpDelete(nameof(Delete))]
    public IActionResult Delete()
    {
        return this.NotImplemented();
    }
}
