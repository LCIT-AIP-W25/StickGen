import unittest
from unittest.mock import patch, MagicMock
from kafka_producer import producer  # Import the producer instance from your Kafka producer script

class TestKafkaProducer(unittest.TestCase):
    @patch('kafka_producer.KafkaProducer')
    def test_producer_instance(self, mock_kafka_producer):
        # Mock KafkaProducer instance
        mock_producer_instance = MagicMock()
        mock_kafka_producer.return_value = mock_producer_instance

        # Verify that the producer instance is created
        self.assertIsNotNone(producer, "Kafka producer instance should not be None")

    @patch('kafka_producer.KafkaProducer')
    def test_send_message(self, mock_kafka_producer):
        # Mock KafkaProducer instance
        mock_producer_instance = MagicMock()
        mock_kafka_producer.return_value = mock_producer_instance

        # Simulate sending a message
        test_message = {"headline": "Test Headline", "content": "Test Content"}
        producer.send("news_topic", value=test_message)

        # Verify that the send method was called with the correct arguments
        mock_producer_instance.send.assert_called_once_with("news_topic", value=test_message)

if __name__ == "__main__":
    unittest.main()