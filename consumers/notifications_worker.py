from consumers.base_worker import BaseWorker

QUEUE_URL = "http://localhost:4566/000000000000/notifications-queue"

class NotificationsWorker(BaseWorker):

    def __init__(self):
        super().__init__(QUEUE_URL, "NOTIFICATIONS")

    def process_message(self, detail):
        self.logger.info(f"[NOTIFICATIONS] Sending notification: {detail}")


if __name__ == "__main__":
    worker = NotificationsWorker()
    worker.run()