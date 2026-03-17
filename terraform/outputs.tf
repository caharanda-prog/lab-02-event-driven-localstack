output "orders_queue_url" {
  value = aws_sqs_queue.orders_queue.id
}

output "payments_queue_url" {
  value = aws_sqs_queue.payments_queue.id
}

output "notifications_queue_url" {
  value = aws_sqs_queue.notifications_queue.id
}

