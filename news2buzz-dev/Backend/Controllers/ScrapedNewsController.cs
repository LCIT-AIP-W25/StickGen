using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using News2Buzz.API.Services;

namespace News2Buzz.API.Controllers
{
    [Route("api/[controller]")]
    [ApiController]

    public class ScrapedNewsController : ControllerBase
    {
        private readonly IScrapedNewsService _service;

        public ScrapedNewsController(IScrapedNewsService service)
        {
            _service = service;
        }

        [HttpGet]

        public async Task<IActionResult> GetAll(
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 10,
    [FromQuery] string title = null,
    [FromQuery] string[] topics = null,
    [FromQuery] string[] biasLabel = null,
    [FromQuery] string[] sentiment = null,
     [FromQuery] DateTime? fromDate = null,
    [FromQuery] DateTime? toDate = null,
    [FromQuery] string[] truthPrediction = null)
        {
            var (data, totalCount) = await _service.GetPaginatedAsync(page, pageSize, title, topics, biasLabel, sentiment, fromDate, toDate, truthPrediction);

            return Ok(new
            {
                TotalCount = totalCount,
                Page = page,
                PageSize = pageSize,
                Data = data
            });
        }


        // GET by ID
        [HttpGet("{id}")]
        public async Task<IActionResult> GetById(int id)
        {
            var news = await _service.GetByIdAsync(id);
            if (news == null) return NotFound();
            return Ok(news);
        }
        [HttpGet("topics")]
        public async Task<IActionResult> GetTopics()
        {
            var topics = await _service.GetDistinctTopicsAsync();
            return Ok(topics);
        }

    }
}
