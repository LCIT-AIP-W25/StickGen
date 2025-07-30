using System;
using Microsoft.ML;
using News2Buzz.API.Models;

namespace News2Buzz.API.Services;

public class SentimentAnalyzer
{
    private readonly MLContext _mlContext;
    private readonly PredictionEngine<SentimentData, SentimentPrediction> _predictionEngine;

    public SentimentAnalyzer()
    {
        _mlContext = new MLContext();

        // Define the data process pipeline
        var dataProcessPipeline = _mlContext.Transforms.Text.FeaturizeText("Features", nameof(SentimentData.Text))
            .Append(_mlContext.BinaryClassification.Trainers.SdcaLogisticRegression());

        // Create training data for basic training
        var trainingData = _mlContext.Data.LoadFromEnumerable(new[]
        {
            new SentimentData { Text = "this is bad", Label = false },
            new SentimentData { Text = "horrible and terrible", Label = false },
            new SentimentData { Text = "really good and excellent", Label = true },
            new SentimentData { Text = "I love this", Label = true },
        });

        var model = dataProcessPipeline.Fit(trainingData);
        _predictionEngine = _mlContext.Model.CreatePredictionEngine<SentimentData, SentimentPrediction>(model);
    }

    public string PredictSentiment(string text)
    {
        var prediction = _predictionEngine.Predict(new SentimentData { Text = text });

        if (prediction.Probability > 0.75) return "positive";
        if (prediction.Probability < 0.45) return "negative";
        return "neutral";
    }
}
