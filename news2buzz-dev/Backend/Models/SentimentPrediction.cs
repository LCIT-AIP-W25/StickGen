using System;
using Microsoft.ML.Data;

namespace News2Buzz.API.Models;

public class SentimentPrediction
{
    [ColumnName("PredictedLabel")]
    public bool Prediction;

    public float Probability { get; set; }
    public float Score { get; set; }
}
