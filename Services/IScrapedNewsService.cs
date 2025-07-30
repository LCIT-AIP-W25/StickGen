using System;
using News2Buzz.API.Models;

namespace News2Buzz.API.Services;

public interface IScrapedNewsService
{
    Task<(IEnumerable<ScrapedNews> Data, int TotalCount)> GetPaginatedAsync(
        int page,
        int pageSize,
        string title,
        string[] topics,
        string[] biasLabels,
        string[] sentiments,
        DateTime? fromDate,
        DateTime? toDate,
        string[] truthPrediction);

    Task<ScrapedNews> GetByIdAsync(int id);
    Task<List<string>> GetDistinctTopicsAsync();

}
