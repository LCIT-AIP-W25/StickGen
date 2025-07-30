using System;
using System.Xml.Linq;
using News2Buzz.API.Models;

namespace News2Buzz.API.Services;

public class RssNewsService : IRssNewsService
{

    public readonly HttpClient _httpClient;
    private readonly Dictionary<string, string> _rssFeeds;
    private readonly SentimentAnalyzer _sentimentAnalyzer;
    public RssNewsService(SentimentAnalyzer sentimentAnalyzer)
    {

        _httpClient = new HttpClient();
        _rssFeeds = new()
        {
            { "Google", "https://news.google.com/rss/search?q={0}&hl=en-US&gl=US&ceid=US:en" },
            { "BBC", "http://feeds.bbci.co.uk/news/rss.xml" },
            { "Reuters", "http://feeds.reuters.com/reuters/topNews" },
            { "CBC", "https://www.cbc.ca/cmlink/rss-world" }
        };
        _sentimentAnalyzer = sentimentAnalyzer;

    }

    public Task<List<ScrapedNews>> FetchAllAsync(string keyword = "")
    {
        throw new NotImplementedException();
    }

    // public async Task<List<ScrapedNews>> FetchAllAsync(string keyword = "")
    // {
    //     var result = new List<ScrapedNews>();
    //     bool hasKeyword = !string.IsNullOrWhiteSpace(keyword);

    //     foreach (var feed in _rssFeeds)
    //     {
    //         if (hasKeyword && !feed.Value.Contains("{0}"))
    //             continue;

    //         string url = feed.Value.Contains("{0}")
    //                        ? string.Format(feed.Value, Uri.EscapeDataString(keyword))
    //                        : feed.Value;


    //         try
    //         {
    //             var response = await _httpClient.GetStringAsync(url);
    //             var doc = XDocument.Parse(response);

    //             var items = doc.Descendants("item").Take(18 );

    //             foreach (var item in items)
    //             {
    //                 var description = item.Element("description")?.Value ?? "";
    //                 var sentiment = _sentimentAnalyzer.PredictSentiment(description);

    //                 result.Add(new ScrapedNews
    //                 {
    //                     Title = item.Element("title")?.Value ?? "",
    //                     Description = item.Element("description")?.Value ?? "",
    //                     Link = item.Element("link")?.Value ?? "",
    //                     PublishedAt = DateTime.TryParse(item.Element("pubDate")?.Value, out var dt) ? dt : DateTime.UtcNow,
    //                     Source = feed.Key,
    //                     ImageUrl = GetImageFromDescription(description),
    //                     Sentiment = sentiment
    //                 });
    //             }
    //         }
    //         catch { continue; }
    //     }

    //     if (!hasKeyword)
    //     {
    //         var rng = new Random();
    //         result = result.OrderBy(_ => rng.Next()).ToList();
    //     }

    //     return result;
    // }

    private string GetImageFromDescription(string html)
    {
        if (string.IsNullOrWhiteSpace(html)) return "";

        var doc = new HtmlAgilityPack.HtmlDocument();
        doc.LoadHtml(html);

        var imgNode = doc.DocumentNode.SelectSingleNode("//img[@src]");
        return imgNode?.GetAttributeValue("src", "") ?? "";
    }



}

