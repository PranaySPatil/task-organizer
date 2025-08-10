output "api_gateway_url" {
  description = "API Gateway endpoint URL"
  value       = "${aws_api_gateway_rest_api.task_api.execution_arn}/prod"
}

output "api_gateway_invoke_url" {
  description = "API Gateway invoke URL"
  value       = "https://${aws_api_gateway_rest_api.task_api.id}.execute-api.${var.aws_region}.amazonaws.com/prod"
}

output "dynamodb_table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.tasks.name
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.task_organizer.function_name
}