import boto3
import json
import logging
import time
import os

class BaseWorker:

    def __init__(self, queue_url, worker_name):
        self.queue_url = queue_url
        self.worker_name = worker_name
        
         # Crear carpeta logs
        os.makedirs("logs", exist_ok=True)

        self.logger = logging.getLogger(worker_name)
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicados
        if not self.logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] [{}] %(message)s".format(worker_name)
            )

            # Archivo
            file_handler = logging.FileHandler(f"logs/{worker_name.lower()}.log")
            file_handler.setFormatter(formatter)

            # Consola
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        self.client = boto3.client(
            "sqs",
            endpoint_url="http://localhost:4566",
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
        )

    def process_message(self, message_body):
        raise NotImplementedError("Implement in subclass")

    def run(self):
        self.logger.info("Starting worker...")

        while True:
            response = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=5
            )

            messages = response.get("Messages", [])

            if not messages:
                continue

            for message in messages:
                try:
                    body = json.loads(message["Body"])

                    # EventBridge envelope
                    detail_type = body.get("detail-type")
                    detail = body.get("detail")

                    self.logger.info(f"Received event: {detail_type} | Payload: {detail}")

                    self.process_message(detail)

                    # delete message
                    self.client.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=message["ReceiptHandle"]
                    )

                    self.logger.info("Message processed and deleted")

                except Exception as e:
                    self.logger.error(f"Error processing message: {str(e)}")

            time.sleep(1)