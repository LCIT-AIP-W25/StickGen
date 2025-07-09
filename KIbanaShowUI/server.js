const express = require("express");
const axios = require("axios");
const cors = require("cors");

const app = express();
app.use(cors()); // Enable CORS for frontend requests

const ELASTICSEARCH_URL = "http://your-elasticsearch-host:9200/news-trends/_search";

app.get("/api/news", async (req, res) => {
  try {
    const response = await axios.get(ELASTICSEARCH_URL);
    const news = response.data.hits.hits.map(hit => hit._source);
    res.json(news);
  } catch (error) {
    console.error("Elasticsearch Fetch Error:", error.message);
    res.status(500).json({ error: error.response?.data || "Error fetching data from Elasticsearch" });
  }
});


app.get("/dashboard", (req, res) => {
  res.redirect("http://your-elasticsearch-host:5601/app/dashboards");
});


app.listen(3000, () => console.log("Server running on port 3000"));
    
  //  This server will listen on port 3000 and fetch news data from Elasticsearch. 
   // Now, let’s run the server: 
   // $ node server.js //