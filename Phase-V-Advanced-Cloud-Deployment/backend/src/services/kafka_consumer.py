import json
import logging
from typing import Callable, Dict, Optional, List
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import confluent_kafka for real Kafka integration
try:
    from confluent_kafka import Consumer, OFFSET_BEGINNING
    CONFLUENT_KAFKA_AVAILABLE = True
except ImportError:
    CONFLUENT_KAFKA_AVAILABLE = False
    logger.warning("confluent-kafka not available - using mock implementation")

class KafkaConsumerService:
    def __init__(self, bootstrap_servers: Optional[str] = None, group_id: str = "dapr-consumer-group"):
        """
        Kafka Consumer Service - supports both real Kafka and mock mode
        
        Args:
            bootstrap_servers: Kafka bootstrap servers (default from env var KAFKA_BOOTSTRAP_SERVERS)
            group_id: Consumer group identifier
        """
        self.bootstrap_servers = bootstrap_servers or os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.group_id = group_id
        self.handlers: Dict[str, List[Callable]] = {}
        self.consumer = None
        self.use_mock = False
        self.subscribed_topics: List[str] = []
        
        if CONFLUENT_KAFKA_AVAILABLE:
            try:
                self.consumer = Consumer({
                    'bootstrap.servers': self.bootstrap_servers,
                    'group.id': group_id,
                    'auto.offset.reset': 'earliest',
                    'enable.auto.commit': True,
                })
                logger.info(f"Initialized real Kafka Consumer with servers: {self.bootstrap_servers}, group: {group_id}")
            except Exception as e:
                logger.warning(f"Failed to initialize real Kafka consumer: {e}. Using mock mode.")
                self.use_mock = True
        else:
            logger.info(f"Using mock Kafka Consumer Service for development (group: {group_id})")
            self.use_mock = True

    def subscribe_to_topics(self, topics: List[str]):
        """Subscribe to Kafka topics"""
        self.subscribed_topics = topics
        
        if self.use_mock or self.consumer is None:
            logger.info(f"[MOCK] Subscribed to topics: {topics}")
        else:
            try:
                self.consumer.subscribe(topics)
                logger.info(f"Subscribed to topics: {topics}")
            except Exception as e:
                logger.error(f"Failed to subscribe to topics: {e}")
                raise

    def register_handler(self, topic: str, handler: Callable):
        """Register a handler function for a specific topic"""
        if topic not in self.handlers:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)
        logger.info(f"Registered handler for topic: {topic}")

    def poll_events(self, timeout: float = 1.0):
        """Poll for events from Kafka"""
        if self.use_mock or self.consumer is None:
            logger.debug(f"[MOCK] Polling for events with timeout {timeout}s")
            return None
        
        try:
            msg = self.consumer.poll(timeout)
            
            if msg is None:
                return None
            
            if msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                return None
            
            # Parse the message
            try:
                event_data = json.loads(msg.value().decode('utf-8'))
                topic = msg.topic()
                
                # Call registered handlers for this topic
                if topic in self.handlers:
                    for handler in self.handlers[topic]:
                        try:
                            handler(event_data)
                        except Exception as e:
                            logger.error(f"Error executing handler for topic {topic}: {e}")
                
                return event_data
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse message: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error polling events: {e}")
            return None

    def poll_events_batch(self, timeout: float = 1.0, max_messages: int = 10) -> List[Dict]:
        """Poll for multiple events from Kafka"""
        messages = []
        
        if self.use_mock or self.consumer is None:
            logger.debug(f"[MOCK] Polling for batch of events (max: {max_messages})")
            return []
        
        try:
            for _ in range(max_messages):
                msg = self.consumer.poll(timeout / max_messages)
                
                if msg is None:
                    break
                
                if msg.error():
                    logger.error(f"Consumer error: {msg.error()}")
                    continue
                
                try:
                    event_data = json.loads(msg.value().decode('utf-8'))
                    topic = msg.topic()
                    
                    # Call registered handlers for this topic
                    if topic in self.handlers:
                        for handler in self.handlers[topic]:
                            try:
                                handler(event_data)
                            except Exception as e:
                                logger.error(f"Error executing handler for topic {topic}: {e}")
                    
                    messages.append(event_data)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse message: {e}")
            
            return messages
        except Exception as e:
            logger.error(f"Error polling events batch: {e}")
            return []

    def close(self):
        """Close the consumer"""
        if not self.use_mock and self.consumer is not None:
            try:
                self.consumer.close()
                logger.info("Closed Kafka Consumer")
            except Exception as e:
                logger.error(f"Error closing consumer: {e}")
        else:
            logger.info("[MOCK] Closed Kafka Consumer")

    def __del__(self):
        """Cleanup when the service is destroyed"""
        self.close()