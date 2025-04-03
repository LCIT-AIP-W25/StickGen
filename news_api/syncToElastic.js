const { MongoClient } = require('mongodb');
const { Client } = require('@elastic/elasticsearch');

const isDocker = process.env.NODE_ENV === 'docker';

const MONGO_URI = isDocker ? 'mongodb://mongodb:27017' : 'mongodb://localhost:27017';
const ES_INDEX = 'news_articles';

const mongoClient = new MongoClient(MONGO_URI);
const esClient = new Client({
  node: isDocker ? 'http://elasticsearch:9200' : 'http://localhost:9200'
});

async function syncData() {
  try {
    await mongoClient.connect();
    console.log('✅ Connected to MongoDB');

    const db = mongoClient.db('news_database');
    const collection = db.collection('news_articles');
    const articles = await collection.find().toArray();

    const indexExists = await esClient.indices.exists({ index: ES_INDEX });
    if (!indexExists) {
      await esClient.indices.create({ index: ES_INDEX });
      console.log('🆕 Created index: news_articles');
    }

    for (const article of articles) {
      const {
        _id,
        headline,
        short_description,
        summary,
        link,
        timestamp,
        cleaned_text,
        sentiment,
        named_entities,
        predicted_category,
        bigrams,
        trigrams
      } = article;

      const doc = {
        headline: headline || "",
        short_description: short_description || "",
        summary: summary || "",
        link: link || "",
        timestamp: timestamp || "",
        cleaned_text: cleaned_text || "",
        sentiment: sentiment || "",
        named_entities: named_entities || [],
        predicted_category: predicted_category || "Uncategorized",
        bigrams: bigrams || "",
        trigrams: trigrams || ""
      };

      await esClient.index({
        index: ES_INDEX,
        id: _id.toString(),
        document: doc
      });
    }

    console.log('✅ All documents synced to Elasticsearch');
  } catch (error) {
    console.error('❌ Error syncing data:', error);
  } finally {
    await mongoClient.close();
  }
}

// ✅ Only run sync if explicitly enabled
if (process.env.ENABLE_SYNC === 'true') {
  syncData();
} else {
  console.log('⏭️ Skipping sync — Logstash is handling MongoDB → Elasticsearch');
}
