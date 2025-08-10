#!/bin/bash

# Deploy AWS infrastructure and Lambda function

set -e

echo "🚀 Deploying Task Organizer to AWS..."

# Create Lambda deployment package
echo "📦 Creating Lambda deployment package..."
cd "$(dirname "$0")"
zip -r task_organizer.zip lambda_function.py

# Deploy with Terraform
echo "🏗️  Deploying infrastructure with Terraform..."
cd terraform
terraform init
terraform plan
terraform apply -auto-approve

# Get API endpoint
API_URL=$(terraform output -raw api_gateway_invoke_url)
echo "✅ Deployment complete!"
echo "📡 API Endpoint: ${API_URL}/task"
echo ""
echo "Update your .env file with:"
echo "TASK_API_ENDPOINT=${API_URL}/task"