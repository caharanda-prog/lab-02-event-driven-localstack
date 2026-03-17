from consumers.base_worker import BaseWorker

QUEUE_URL = "http://localhost:4566/000000000000/payments-queue"

class PaymentsWorker(BaseWorker):

    def __init__(self):
        super().__init__(QUEUE_URL, "PAYMENTS")

    def process_message(self, detail):
        self.logger.info(f"[PAYMENTS] Processing payment: {detail}")


if __name__ == "__main__":
    worker = PaymentsWorker()
    worker.run()