using System;
using Microsoft.EntityFrameworkCore;
using News2Buzz.API.Data;
using News2Buzz.API.Models;
using Org.BouncyCastle.Crypto.Paddings;

namespace News2Buzz.API.Services;

public class ScrapedNewsService : IScrapedNewsService
{
    private readonly AppDbContext _context;
    public ScrapedNewsService(AppDbContext context)
    {
        _context = context;
    }
    public async Task<(IEnumerable<ScrapedNews> Data, int TotalCount)> GetPaginatedAsync(
    int page,
    int pageSize,
    string title,
    string[] topics,
    string[] biasLabels,
    string[] sentiments,
    DateTime? fromDate,
    DateTime? toDate, string[] truthPrediction)
    {
        var query = _context.ScrapedNews.AsQueryable();

        if (!string.IsNullOrWhiteSpace(title))
            query = query.Where(n => n.Title.Contains(title));

        if (topics != null && topics.Length > 0)
            query = query.Where(n => topics.Contains(n.Topic));

        if (biasLabels != null && biasLabels.Length > 0)
            query = query.Where(n => biasLabels.Contains(n.BiasLabel.ToLower()));

        if (sentiments != null && sentiments.Length > 0)
            query = query.Where(n => sentiments.Contains(n.Sentiment.ToLower()));

        if (fromDate.HasValue)
            query = query.Where(n => n.Timestamp >= fromDate.Value);

        if (toDate.HasValue)
            query = query.Where(n => n.Timestamp <= toDate.Value.Date.AddDays(1).AddSeconds(-1));

        if (truthPrediction != null && truthPrediction.Length > 0)
            query = query.Where(x => truthPrediction.Contains(x.TruthPrediction.ToLower()));


        var totalCount = await query.CountAsync();

        var data = await query
            .OrderByDescending(n => n.Timestamp)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return (data, totalCount);

    }


    public async Task<ScrapedNews> GetByIdAsync(int id)
    {
        return await _context.ScrapedNews.FindAsync(id);
    }

    public async Task<List<string>> GetDistinctTopicsAsync()
    {
        return await _context.ScrapedNews
            .Where(n => !string.IsNullOrEmpty(n.Topic))
            .Select(n => n.Topic)
            .Distinct()
            .OrderBy(t => t)
            .ToListAsync();
    }

}
