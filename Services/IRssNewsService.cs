using System;
using News2Buzz.API.Models;

namespace News2Buzz.API.Services;

public interface IRssNewsService
{
    Task<List<ScrapedNews>> FetchAllAsync(string keyword = "");
}
