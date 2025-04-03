const { Client } = require('@elastic/elasticsearch');

const client = new Client({ node: 'http://elasticsearch:9200' });

exports.getNews = async (req, res) => {
  const { query } = req.query;

  try {
    let response;

    if (query && query.trim() !== "") {
      // Search with keyword
      response = await client.search({
        index: 'news_articles',
        query: {
          multi_match: {
            query,
            fields: ['headline', 'short_description', 'summary','predicted_category']
          }
        }
      });
    } else {
      // Return all news when query is empty
      response = await client.search({
        index: 'news_articles',
        size: 100, // Fetch up to 100 articles
        query: {
          match_all: {}
        }
      });
    }

    const hits = response.hits.hits.map(hit => hit._source);
    res.json(hits);
  } catch (err) {
    console.error("Elasticsearch query failed:", err);
    res.status(500).json({ error: "Failed to fetch news" });
  }
};
