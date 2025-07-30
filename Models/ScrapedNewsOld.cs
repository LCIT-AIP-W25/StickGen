using System;

namespace News2Buzz.API.Models;

public class ScrapedNewsOld
{
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Link { get; set; } = string.Empty;
    public string Source { get; set; } = string.Empty;
    public DateTime PublishedAt { get; set; }
    public string ImageUrl { get; set; } = string.Empty;
    public string Sentiment { get; set; } = string.Empty;

}
