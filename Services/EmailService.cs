using System.Net.Http;
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.Configuration;

public class EmailService : IEmailService
{
    private readonly IConfiguration _config;
    private readonly HttpClient _httpClient;

    public EmailService(IConfiguration config)
    {
        _config = config;
        _httpClient = new HttpClient();
    }

    public async Task SendEmailAsync(string toEmail, string subject, string body)
    {
        var apiKey = _config["Mailtrap:ApiKey"];
        var senderEmail = _config["Mailtrap:Sender"];

        Console.WriteLine("📬 Mailtrap API Key: " + apiKey); // TEMP: Check if the key is read correctly

        var requestBody = new
        {
            to = new[] { new { email = toEmail } },
            from = new { email = senderEmail },
            subject = subject,
            html = body
        };

        var content = new StringContent(JsonSerializer.Serialize(requestBody), Encoding.UTF8, "application/json");

        _httpClient.DefaultRequestHeaders.Clear();
        _httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {apiKey}"); // ✅ Correct header

        var response = await _httpClient.PostAsync("https://send.api.mailtrap.io/api/send", content);

        if (!response.IsSuccessStatusCode)
        {
            var errorContent = await response.Content.ReadAsStringAsync();
            Console.WriteLine("❌ Mailtrap API Error: " + errorContent);
        }

        response.EnsureSuccessStatusCode();
    }


}
