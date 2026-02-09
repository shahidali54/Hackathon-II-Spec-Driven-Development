"""
Notification Service
Handles sending reminders and notifications based on task due dates.
Subscribes to reminder-events from Kafka and processes reminder notifications.
"""
import asyncio
import logging
import os
import httpx
from datetime import datetime
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
    title="Notification Service",
    description="Handles reminder and notification event processing",
    version="1.0.0"
)

# Configuration
MAIN_API_URL = os.getenv('MAIN_API_URL', 'http://localhost:8000')
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'localhost:9092')

class NotificationProcessor:
    """Processes reminder events from Kafka"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)
        self.sent_count = 0
        self.failed_count = 0
    
    async def send_reminder(self, task_id: str, user_id: str, reminder_time: str) -> bool:
        """
        Send a reminder notification.
        In a real implementation, this would send email, push notifications, SMS, etc.
        """
        try:
            logger.info(f"Processing reminder for task {task_id} to user {user_id}")
            logger.info(f"Reminder time: {reminder_time}")
            
            # Simulate sending notification (in real app: send email, push, SMS, etc.)
            # For now, we'll just log it
            logger.info(f"✉️ [MOCK] Would send reminder notification for task {task_id} to user {user_id}")
            
            # In a production system, you might:
            # 1. Fetch user preferences (notification channels)
            # 2. Send email via email service
            # 3. Send push notification via push service
            # 4. Send SMS via SMS service
            # 5. Mark reminder as sent in database
            
            self.sent_count += 1
            return True
            
        except Exception as e:
            logger.error(f"Error sending reminder for task {task_id}: {str(e)}")
            self.failed_count += 1
            return False
    
    async def mark_reminder_sent(self, reminder_id: str) -> bool:
        """Mark a reminder as sent in the main API"""
        try:
            logger.info(f"Marking reminder {reminder_id} as sent")
            # Would call main API to update reminder status
            return True
        except Exception as e:
            logger.error(f"Error marking reminder {reminder_id} as sent: {str(e)}")
            return False

# Initialize processor
processor = NotificationProcessor()

@app.on_startup
async def startup_event():
    logger.info("Notification Service starting up...")
    logger.info(f"Main API URL: {MAIN_API_URL}")
    logger.info(f"Kafka Brokers: {KAFKA_BROKERS}")

@app.on_shutdown
async def shutdown_event():
    logger.info("Notification Service shutting down...")
    logger.info(f"Sent {processor.sent_count} reminders, {processor.failed_count} failed")
    await processor.client.aclose()

@app.post("/handle-reminder-event")
async def handle_reminder_event(event_data: Dict[str, Any]):
    """
    Handle reminder events from Kafka.
    Called by Dapr when a message is received on the reminders topic.
    """
    try:
        logger.info(f"Received reminder event: {event_data}")
        
        event_type = event_data.get('event_type', '')
        task_id = event_data.get('task_id', '')
        user_id = event_data.get('user_id', '')
        reminder_time = event_data.get('reminder_time', '')
        
        if event_type == 'reminder_triggered':
            success = await processor.send_reminder(task_id, user_id, reminder_time)
            if success:
                return {"status": "sent", "task_id": task_id}
            else:
                return {"status": "failed", "task_id": task_id}
        
        return {"status": "ignored", "event_type": event_type}
        
    except Exception as e:
        logger.error(f"Error processing reminder event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "notification-service",
        "timestamp": datetime.utcnow().isoformat(),
        "reminders_sent": processor.sent_count,
        "reminders_failed": processor.failed_count
    }

@app.get("/metrics")
async def metrics():
    """Metrics endpoint"""
    return {
        "service": "notification-service",
        "reminders_sent": processor.sent_count,
        "reminders_failed": processor.failed_count,
        "success_rate": (
            processor.sent_count / (processor.sent_count + processor.failed_count)
            if (processor.sent_count + processor.failed_count) > 0
            else 0
        )
    }

# Main entry point
if __name__ == '__main__':
    port = int(os.getenv('PORT', '8002'))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
