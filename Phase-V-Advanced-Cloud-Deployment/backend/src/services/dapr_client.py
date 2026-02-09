import json
import logging
from typing import Any, Dict, Optional
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Dapr SDK
try:
    from dapr.clients import DaprClient
    from dapr.ext.fastapi import DaprMiddleware
    from dapr.ext.fastapi import HTTPExtension
    DAPR_SDK_AVAILABLE = True
except ImportError:
    DAPR_SDK_AVAILABLE = False
    logger.warning("Dapr SDK not available - using mock implementation")

class DaprClientService:
    """Service for interacting with Dapr runtime"""
    
    def __init__(self):
        self.client = None
        self.use_mock = False
        self.dapr_host = os.getenv('DAPR_HOST', 'localhost')
        self.dapr_port = os.getenv('DAPR_HTTP_PORT', '3500')
        self.dapr_grpc_port = os.getenv('DAPR_GRPC_PORT', '50001')
        
    def __enter__(self):
        if DAPR_SDK_AVAILABLE:
            try:
                from dapr.clients import DaprClient
                self.client = DaprClient(
                    dapr_host=self.dapr_host,
                    dapr_grpc_port=int(self.dapr_grpc_port)
                )
                logger.info(f"Connected to Dapr at {self.dapr_host}:{self.dapr_grpc_port}")
            except Exception as e:
                logger.warning(f"Failed to connect to Dapr: {e}. Using mock mode.")
                self.use_mock = True
        else:
            logger.info("Using mock Dapr Client Service")
            self.use_mock = True
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            try:
                self.client.close()
            except Exception as e:
                logger.error(f"Error closing Dapr client: {e}")

    @staticmethod
    def get_client():
        """Get a Dapr client instance (context manager handle)"""
        service = DaprClientService()
        return service.__enter__()

    @staticmethod
    def publish_event(pubsub_name: str, topic_name: str, data: Dict[str, Any]):
        """Publish an event using Dapr pub/sub"""
        with DaprClientService() as service:
            if service.use_mock:
                logger.info(f"[MOCK] Published event to {pubsub_name}/{topic_name}: {data}")
                return
            
            try:
                if service.client:
                    service.client.publish_event(
                        pubsub_name=pubsub_name,
                        topic_name=topic_name,
                        data=json.dumps(data),
                        data_content_type='application/json'
                    )
                    logger.info(f"Published event to {pubsub_name}/{topic_name}")
            except Exception as e:
                logger.error(f"Failed to publish event: {str(e)}")
                raise

    @staticmethod
    def invoke_service(method: str, service_url: str, data: Optional[Dict[str, Any]] = None):
        """Invoke another service using Dapr service invocation"""
        with DaprClientService() as service:
            if service.use_mock:
                logger.info(f"[MOCK] Invoked service {service_url} with method {method}")
                return {"status": "mock", "data": data}
            
            try:
                if service.client:
                    from dapr.ext.fastapi import HTTPExtension
                    
                    # Determine the HTTP method
                    http_method = method.upper()
                    http_ext = getattr(HTTPExtension, http_method, HTTPExtension.POST)
                    
                    resp = service.client.invoke_method(
                        method=method,
                        service_url=service_url,
                        data=json.dumps(data) if data else None,
                        http_extension=http_ext
                    )
                    
                    logger.info(f"Invoked service {service_url} with method {method}")
                    return resp
            except Exception as e:
                logger.error(f"Failed to invoke service: {str(e)}")
                raise

    @staticmethod
    def get_secret(store_name: str, key: str):
        """Get a secret from Dapr secret store"""
        with DaprClientService() as service:
            if service.use_mock:
                logger.info(f"[MOCK] Retrieved secret from {store_name}/{key}")
                return {"key": key, "value": "mock_value"}
            
            try:
                if service.client:
                    resp = service.client.get_secret(
                        store_name=store_name,
                        key=key
                    )
                    logger.info(f"Retrieved secret from {store_name}/{key}")
                    return resp
            except Exception as e:
                logger.error(f"Failed to get secret: {str(e)}")
                raise

    @staticmethod
    def save_state(store_name: str, key: str, value: Any):
        """Save state using Dapr state store"""
        with DaprClientService() as service:
            if service.use_mock:
                logger.info(f"[MOCK] Saved state to {store_name}/{key}: {value}")
                return
            
            try:
                if service.client:
                    service.client.save_state(
                        store_name=store_name,
                        key=key,
                        value=json.dumps(value) if not isinstance(value, str) else value
                    )
                    logger.info(f"Saved state to {store_name}/{key}")
            except Exception as e:
                logger.error(f"Failed to save state: {str(e)}")
                raise

    @staticmethod
    def get_state(store_name: str, key: str):
        """Get state from Dapr state store"""
        with DaprClientService() as service:
            if service.use_mock:
                logger.info(f"[MOCK] Retrieved state from {store_name}/{key}")
                return None
            
            try:
                if service.client:
                    resp = service.client.get_state(
                        store_name=store_name,
                        key=key
                    )
                    logger.info(f"Retrieved state from {store_name}/{key}")
                    return resp
            except Exception as e:
                logger.error(f"Failed to get state: {str(e)}")
                return None

    @staticmethod
    def delete_state(store_name: str, key: str):
        """Delete state from Dapr state store"""
        with DaprClientService() as service:
            if service.use_mock:
                logger.info(f"[MOCK] Deleted state from {store_name}/{key}")
                return
            
            try:
                if service.client:
                    service.client.delete_state(
                        store_name=store_name,
                        key=key
                    )
                    logger.info(f"Deleted state from {store_name}/{key}")
            except Exception as e:
                logger.error(f"Failed to delete state: {str(e)}")
                raise