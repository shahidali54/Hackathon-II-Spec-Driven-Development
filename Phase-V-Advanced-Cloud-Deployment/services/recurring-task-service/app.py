"""
Recurring Task Service
Handles the creation of new task instances when recurring tasks are completed.
Subscribes to task-events from Kafka and processes recurring task completions.
"""
import asyncio
import logging
import os
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
from fastapi import FastAPI, HTTPException
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Recurring Task Service",
    description="Handles recurring task event processing",
    version="1.0.0"
)

# Configuration
MAIN_API_URL = os.getenv('MAIN_API_URL', 'http://localhost:8000')
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'localhost:9092')

class RecurringTaskProcessor:
    """Processes recurring task events from Kafka"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)
    
    async def process_completed_task(self, task_id: str, payload: Dict[str, Any]) -> bool:
        """
        Process a completed recurring task.
        Creates the next occurrence if the task has a recurrence rule.
        """
        try:
            logger.info(f"Processing completed recurring task: {task_id}")
            
            # In a real implementation with proper auth, you would:
            # 1. Get the task details from the main API
            # 2. Check if it has a recurrence rule
            # 3. Calculate next occurrence
            # 4. Create a new task
            
            # For now, we'll just log the event
            has_recurrence = payload.get('has_recurrence', False)
            
            if has_recurrence:
                logger.info(f"Task {task_id} has recurrence rule, would create next occurrence")
                # This would be called by the task service when processing the event
                # The actual creation is handled by the main API
            else:
                logger.info(f"Task {task_id} is not recurring, no action needed")
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing recurring task {task_id}: {str(e)}")
            return False
    
    async def handle_recurring_task_generated(self, task_id: str) -> bool:
        """Handle a newly generated recurring task"""
        try:
            logger.info(f"New recurring task generated: {task_id}")
            # Could publish an event or log for monitoring
            return True
        except Exception as e:
            logger.error(f"Error handling generated task {task_id}: {str(e)}")
            return False

# Initialize processor
processor = RecurringTaskProcessor()

@app.on_startup
async def startup_event():
    logger.info("Recurring Task Service starting up...")
    logger.info(f"Main API URL: {MAIN_API_URL}")
    logger.info(f"Kafka Brokers: {KAFKA_BROKERS}")

@app.on_shutdown
async def shutdown_event():
    logger.info("Recurring Task Service shutting down...")
    await processor.client.aclose()

@app.post("/handle-task-event")
async def handle_task_event(event_data: Dict[str, Any]):
    """
    Handle task events from Kafka.
    Called by Dapr when a message is received on the task-events topic.
    """
    try:
        logger.info(f"Received task event: {event_data}")
        
        event_type = event_data.get('event_type', '')
        task_id = event_data.get('task_id', '')
        user_id = event_data.get('user_id', '')
        payload = event_data.get('payload', {})
        
        if event_type == 'task_completion_toggled':
            if payload.get('is_completed') and payload.get('has_recurrence'):
                success = await processor.process_completed_task(task_id, payload)
                if success:
                    return {"status": "processed", "task_id": task_id}
                else:
                    return {"status": "error", "task_id": task_id}
        
        elif event_type == 'recurring_task_generated':
            success = await processor.handle_recurring_task_generated(task_id)
            if success:
                return {"status": "handled", "task_id": task_id}
        
        return {"status": "ignored", "event_type": event_type}
        
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "recurring-task-service",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/metrics")
async def metrics():
    """Basic metrics endpoint"""
    return {
        "service": "recurring-task-service",
        "uptime": "tracking available",
        "events_processed": "tracking available"
    }

# Main entry point
if __name__ == '__main__':
    port = int(os.getenv('PORT', '8001'))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
