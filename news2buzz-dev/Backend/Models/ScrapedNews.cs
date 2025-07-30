using System;

namespace News2Buzz.API.Models;

public class ScrapedNews
{
    public int Id { get; set; }
    public string Title { get; set; }
    public string Summary { get; set; }
    public string Link { get; set; }
    public DateTime? Timestamp { get; set; }
    public string Source { get; set; }
    public DateTime ScrapedAt { get; set; }
    public string Topic { get; set; }
    public string BiasLabel { get; set; }
    public string Sentiment { get; set; }
    public string TruthPrediction { get; set; }
}
