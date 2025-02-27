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
    res.status(500).json({ error: "Error fetching data from Elasticsearch" });
  }
});

app.listen(3000, () => console.log("Server running on port 3000"));
