import unittest
from unittest.mock import patch, MagicMock
from kafka import KafkaConsumer
from pymongo import MongoClient
import kafka_consumer  # Import the consumer script

class TestKafkaConsumer(unittest.TestCase):
    @patch('kafka_consumer.KafkaConsumer')
    @patch('kafka_consumer.MongoClient')
    def test_consumer_inserts_message_to_mongodb(self, mock_mongo_client, mock_kafka_consumer):
        # Mock KafkaConsumer
        mock_consumer_instance = MagicMock()
        mock_kafka_consumer.return_value = mock_consumer_instance
        mock_consumer_instance.__iter__.return_value = [
            MagicMock(value=b'{"headline": "Test Headline", "content": "Test Content"}')
        ]

        # Mock MongoDB
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_mongo_client.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection

        # Run the consumer script
        kafka_consumer.main()

        # Verify that the message was inserted into MongoDB
        mock_collection.insert_one.assert_called_once_with({
            "headline": "Test Headline",
            "content": "Test Content"
        })

if __name__ == "__main__":
    unittest.main()