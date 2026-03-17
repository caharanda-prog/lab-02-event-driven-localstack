# Lab 02 - Event-Driven Architecture with LocalStack

## 📌 Overview

This lab demonstrates an event-driven architecture using AWS services simulated locally with LocalStack.

It showcases how to design loosely coupled systems using EventBridge for event routing and SQS queues for asynchronous processing, without requiring an AWS account.

The solution includes infrastructure provisioning with Terraform, a Python-based producer, and multiple consumers to simulate real-world event flow across services.

---

## 🧠 Architecture Overview

The system is composed of the following components:

* **Producer**
  Generates domain events such as:

  * `OrderCreated`
  * `PaymentCompleted`

* **EventBridge**
  Acts as the central event bus, responsible for routing events to different targets based on rules.

* **Event Rules**
  Define how events are filtered and routed:

  * Orders rule → Orders queue
  * Payments rule → Payments queue
  * Notifications rule → Notifications queue (cross-cutting concern)

* **SQS Queues**

  * Orders Queue
  * Payments Queue
  * Notifications Queue

* **Consumers (Workers)**

  * Orders Worker → processes order-related events
  * Payments Worker → processes payment-related events
  * Notifications Worker → processes all relevant events for notifications

Each consumer works independently, reinforcing a loosely coupled architecture.

---

## 📊 Architecture Diagram

> TODO: Add architecture diagram here (PNG or SVG)

---

## ⚙️ Tech Stack

* Terraform
* LocalStack
* AWS CLI
* Python (boto3)
* Docker

---

## 📁 Project Structure

```
.
├── terraform/
│   └── main.tf
│   └── provider.tf
│   └── outputs.tf
│   └── variables.tf
│
├── producers/
│   └── producer.py
│
├── consumers/
│   ├── _init_.py
│   ├── base_worker.py
│   ├── orders_worker.py
│   ├── payments_worker.py
│   └── notifications_worker.py
│
├── scripts/
│   └── start_consumers.ps1
│
├── logs/
│   └── (generated at runtime)
│
└── README.md
```

---

## 🚀 How to Run

### 1. Start LocalStack

```bash
docker run -d -p 4566:4566 localstack/localstack
```

---

### 2. Provision Infrastructure

```bash
cd terraform
terraform init
terraform apply -auto-approve
```

This will create:

* EventBridge bus
* Event rules
* SQS queues
* Targets connecting rules to queues

---

### 3. Run Producer

```bash
python producer/producer.py
```

The producer will:

* Send events every few seconds
* Generate a mix of `OrderCreated` and `PaymentCompleted`
* Run for a fixed duration (~2 minutes)
* Generates random events at ~5-second intervals

---

### 4. Start Consumers

You can start all consumers using the provided PowerShell script:

```bash
./scripts/start_consumers.ps1
```

This will launch all workers (orders, payments, notifications) in separate terminals.

---

Alternatively, you can run each worker manually in different terminals:

```bash
python -m consumers.orders_worker
```

```bash
python -m consumers.payments_worker
```

```bash
python -m consumers.notifications_worker
```

---

Each worker will:

* Continuously poll its assigned SQS queue  
* Process incoming messages independently  
* Log results to file for traceability  

> ⚠️ **Note:**  
> Consumers in this lab are intentionally simple.  
> Their responsibility is limited to retrieving messages from SQS, logging the event content, and deleting the message after processing.  
> No business logic is implemented, as the focus is on event flow, routing, and system design rather than domain-specific behavior.

---

## 🔄 Event Flow

1. The **Producer** sends events to EventBridge
2. **EventBridge** evaluates routing rules
3. Events are forwarded to corresponding **SQS queues**
4. **Consumers** poll their queues independently
5. Messages are processed and logged
6. Messages are deleted after successful processing

---

## 📊 Observability (Queues)

You can verify messages in queues using AWS CLI:

```bash
aws --endpoint-url=http://localhost:4566 sqs get-queue-attributes --queue-url <QUEUE_URL> --attribute-names ApproximateNumberOfMessages
```

Expected behavior:

* Messages accumulate if consumers are stopped
* Messages decrease as consumers process them

---

## 🧾 Logging

Each worker writes logs to file:

```
logs/
├── orders_worker.log
├── payments_worker.log
└── notifications_worker.log
└── producer.log
```

Logs include:

* Worker startup
* Message processing
* Event details

---

## 🧪 What This Lab Demonstrates

* Event-driven architecture patterns
* Asynchronous communication
* Event routing with EventBridge
* Decoupled services using queues
* Independent consumers (workers)
* Infrastructure as Code with Terraform
* Local cloud simulation using LocalStack

---

## 🎯 Key Concepts

* **Loose Coupling**
  Producers and consumers do not depend on each other directly

* **Event Routing**
  Rules determine where events should go

* **Scalability**
  Consumers can scale independently

* **Extensibility**
  New consumers can be added without modifying existing ones

---

## 🧼 Clean Up

```bash
cd terraform
terraform destroy -auto-approve
```

---

## 📎 Notes

* This lab runs entirely locally using LocalStack
* No AWS account is required
* Focus is on architecture rather than language-specific implementation
* Designed to simulate real-world cloud patterns in a controlled environment

---

