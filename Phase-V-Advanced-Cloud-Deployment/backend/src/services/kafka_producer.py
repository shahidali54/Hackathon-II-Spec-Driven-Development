import json
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import confluent_kafka for real Kafka integration
try:
    from confluent_kafka import Producer
    CONFLUENT_KAFKA_AVAILABLE = True
except ImportError:
    CONFLUENT_KAFKA_AVAILABLE = False
    logger.warning("confluent-kafka not available - using mock implementation")

class KafkaProducerService:
    def __init__(self, bootstrap_servers: Optional[str] = None):
        """
        Kafka Producer Service - supports both real Kafka and mock mode
        
        Args:
            bootstrap_servers: Kafka bootstrap servers (default from env var KAFKA_BOOTSTRAP_SERVERS)
        """
        self.bootstrap_servers = bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.producer = None
        self.use_mock = False
        
        if CONFLUENT_KAFKA_AVAILABLE:
            try:
                self.producer = Producer({
                    'bootstrap.servers': self.bootstrap_servers,
                    'client.id': 'todo-app-producer',
                    'acks': 'all',
                    'retries': 3,
                })
                logger.info(f"Initialized real Kafka Producer with servers: {self.bootstrap_servers}")
            except Exception as e:
                logger.warning(f"Failed to initialize real Kafka producer: {e}. Using mock mode.")
                self.use_mock = True
        else:
            logger.info("Using mock Kafka Producer Service for development")
            self.use_mock = True

    def delivery_report(self, err, msg):
        """Delivery report callback function"""
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def publish_event(self, topic: str, event_data: Dict[str, Any]):
        """Publish an event to Kafka"""
        try:
            # Convert event data to JSON string
            event_json = json.dumps(event_data)
            
            if self.use_mock or self.producer is None:
                # Mock implementation
                logger.info(f"[MOCK] Published event to topic '{topic}': {event_data}")
            else:
                # Real Kafka implementation
                self.producer.produce(
                    topic=topic,
                    key=event_data.get('user_id', 'unknown').encode('utf-8'),
                    value=event_json.encode('utf-8'),
                    callback=self.delivery_report
                )
                logger.info(f"Published event to topic '{topic}': {event_data}")
                
        except Exception as e:
            logger.error(f"Failed to publish event to topic {topic}: {str(e)}")
            raise

    def publish_task_event(self, task_id: str, event_type: str, user_id: str, payload: Optional[Dict[str, Any]] = None):
        """Publish a task-related event to the task-events topic"""
        event_data = {
            "event_type": event_type,
            "task_id": task_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": payload or {}
        }
        self.publish_event("task-events", event_data)

    def publish_reminder_event(self, task_id: str, reminder_time: str, user_id: str):
        """Publish a reminder event to the reminders topic"""
        event_data = {
            "event_type": "reminder_triggered",
            "task_id": task_id,
            "user_id": user_id,
            "reminder_time": reminder_time,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.publish_event("reminders", event_data)

    def publish_recurring_task_event(self, task_id: str, next_occurrence: str, user_id: str):
        """Publish a recurring task event to the task-events topic"""
        event_data = {
            "event_type": "recurring_task_generated",
            "task_id": task_id,
            "user_id": user_id,
            "next_occurrence": next_occurrence,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        self.publish_event("task-events", event_data)

    def flush(self, timeout: int = 10):
        """Wait for all messages to be delivered"""
        if not self.use_mock and self.producer is not None:
            try:
                remaining = self.producer.flush(timeout)
                if remaining > 0:
                    logger.warning(f"Timed out waiting for {remaining} message(s) to deliver")
            except Exception as e:
                logger.error(f"Error flushing producer: {str(e)}")
        else:
            logger.info("Mock producer - no need to flush")

    def __del__(self):
        """Cleanup when the service is destroyed"""
        self.flush()