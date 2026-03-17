import boto3
import json
import time
import random
import uuid
import logging
import os
from datetime import datetime

# =========================
# CONFIG LOGGING
# =========================
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("PRODUCER")
logger.setLevel(logging.INFO)

if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [PRODUCER] %(message)s"
    )

    file_handler = logging.FileHandler("logs/producer.log")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# =========================
# CONFIG AWS (LocalStack)
# =========================
EVENT_BUS_NAME = "default"

client = boto3.client(
    "events",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

# =========================
# EVENT GENERATOR
# =========================
def generate_order_created():
    return {
        "orderId": str(uuid.uuid4()),
        "amount": random.randint(100, 500),
        "currency": "MXN",
        "createdAt": datetime.utcnow().isoformat()
    }

def generate_payment_completed():
    return {
        "paymentId": str(uuid.uuid4()),
        "orderId": str(uuid.uuid4()),
        "amount": random.randint(100, 500),
        "status": "COMPLETED",
        "processedAt": datetime.utcnow().isoformat()
    }

# =========================
# SEND EVENT
# =========================
def send_event(detail_type, detail):
    event = {
        "Source": "lab.ecommerce",
        "DetailType": detail_type,
        "Detail": json.dumps(detail),
        "EventBusName": EVENT_BUS_NAME
    }

    response = client.put_events(Entries=[event])

    logger.info(f"Sent event: {detail_type} | Response: {response}")

# =========================
# MAIN LOOP
# =========================
def run_producer(duration_seconds=120, interval_seconds=5):
    logger.info("Starting producer...")

    start_time = time.time()

    while (time.time() - start_time) < duration_seconds:

        event_type = random.choice(["OrderCreated", "PaymentCompleted"])

        if event_type == "OrderCreated":
            detail = generate_order_created()
        else:
            detail = generate_payment_completed()

        logger.info(f"Generating event: {event_type} | Payload: {detail}")

        send_event(event_type, detail)

        time.sleep(interval_seconds)

    logger.info("Producer finished.")

# =========================
# ENTRYPOINT
# =========================
if __name__ == "__main__":
    run_producer()