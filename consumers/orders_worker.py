from consumers.base_worker import BaseWorker

QUEUE_URL = "http://localhost:4566/000000000000/orders-queue"

class OrdersWorker(BaseWorker):

    def __init__(self):
        super().__init__(QUEUE_URL, "ORDERS")

    def process_message(self, detail):
        self.logger.info(f"[ORDERS] Processing order: {detail}")


if __name__ == "__main__":
    worker = OrdersWorker()
    worker.run()