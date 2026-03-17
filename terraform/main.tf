resource "aws_sqs_queue" "orders_queue" {
  name = "orders-queue"
}

resource "aws_sqs_queue" "payments_queue" {
  name = "payments-queue"
}

resource "aws_sqs_queue" "notifications_queue" {
  name = "notifications-queue"
}

resource "aws_cloudwatch_event_rule" "order_created_rule" {

  name = "order-created-rule"

  event_pattern = jsonencode({
    "detail-type": ["OrderCreated"]
  })

}

resource "aws_cloudwatch_event_rule" "payment_completed_rule" {

  name = "payment-completed-rule"

  event_pattern = jsonencode({
    "detail-type": ["PaymentCompleted"]
  })

}

resource "aws_cloudwatch_event_target" "orders_target" {

  rule      = aws_cloudwatch_event_rule.order_created_rule.name
  target_id = "orders-target"
  arn       = aws_sqs_queue.orders_queue.arn

}

resource "aws_cloudwatch_event_target" "notifications_order_target" {

  rule      = aws_cloudwatch_event_rule.order_created_rule.name
  target_id = "notifications-order-target"
  arn       = aws_sqs_queue.notifications_queue.arn

}

resource "aws_cloudwatch_event_target" "payments_target" {

  rule      = aws_cloudwatch_event_rule.payment_completed_rule.name
  target_id = "payments-target"
  arn       = aws_sqs_queue.payments_queue.arn

}

resource "aws_cloudwatch_event_target" "notifications_payment_target" {

  rule      = aws_cloudwatch_event_rule.payment_completed_rule.name
  target_id = "notifications-payment-target"
  arn       = aws_sqs_queue.notifications_queue.arn

}





