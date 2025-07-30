using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using News2Buzz.API.Services;

namespace News2Buzz.API.Controllers
{
    [Route("api/rss")]
    [ApiController]
    public class RssNewsController : ControllerBase
    {
        private readonly IRssNewsService _rssService;
        public RssNewsController(IRssNewsService rssService)
        {
            _rssService = rssService;
        }
        [HttpGet("fetch")]
        public async Task<IActionResult> FetchNews([FromQuery] string keyword = "")
        {
            var result = await _rssService.FetchAllAsync(keyword);
            return Ok(result);
        }
    }
}
