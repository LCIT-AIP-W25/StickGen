using System;
using Microsoft.ML.Data;

namespace News2Buzz.API.Models;

public class SentimentData
{
    [LoadColumn(0)]
    public string Text;

    [LoadColumn(1), ColumnName("Label")]
    public bool Label;
}
