# WhatsApp Integration Setup

## Prerequisites
- Twilio account
- WhatsApp Business API access (or Twilio Sandbox)

## Setup Steps

### 1. Twilio Configuration
1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to **Messaging** → **Try it out** → **Send a WhatsApp message**
3. Follow sandbox setup instructions
4. Note your sandbox WhatsApp number

### 2. Deploy Webhook Lambda
```bash
# Create deployment package
zip whatsapp_webhook.zip whatsapp_webhook.py

# Deploy with AWS CLI
aws lambda create-function \
  --function-name whatsapp-task-webhook \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler whatsapp_webhook.lambda_handler \
  --zip-file fileb://whatsapp_webhook.zip \
  --environment Variables='{TASK_API_ENDPOINT=YOUR_TASK_API_ENDPOINT}'
```

### 3. Create API Gateway for Webhook
```bash
# Get function ARN
aws lambda get-function --function-name whatsapp-task-webhook

# Create API Gateway (or use Terraform)
# Set webhook URL in Twilio console
```

### 4. Configure Twilio Webhook
1. In Twilio Console, go to **Phone Numbers** → **Manage** → **WhatsApp senders**
2. Click on your WhatsApp number
3. Set webhook URL to your API Gateway endpoint
4. Set HTTP method to POST

### 5. Test
1. Send WhatsApp message to your Twilio number: "Buy milk"
2. Should receive organized task confirmation
3. Check Obsidian vault for new task

## Environment Variables
```
TASK_API_ENDPOINT=https://your-api-gateway.amazonaws.com/prod/task
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
```

## Message Format
Users can send any natural language task:
- "Buy groceries"
- "Call dentist tomorrow"
- "Finish project report by Friday"

The system will automatically categorize and prioritize.