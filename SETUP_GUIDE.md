# Task Organizer Setup Guide

Complete setup guide for the AI-powered task organization system.

## Prerequisites

- AWS Account with CLI configured
- Python 3.9+
- Terraform (for infrastructure)
- Obsidian installed
- Alfred (for Mac integration)

## Step-by-Step Setup

### 1. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values
nano .env
```

Required variables:
- `AWS_REGION`: Your AWS region (e.g., us-east-1)
- `OBSIDIAN_VAULT_PATH`: Path to your Obsidian vault
- `TASK_API_ENDPOINT`: Will be set after AWS deployment

### 2. AWS Infrastructure Deployment

```bash
# Deploy AWS resources
cd aws
./deploy.sh

# Note the API endpoint from output
# Update .env with TASK_API_ENDPOINT
```

### 3. Mac Integration Setup

```bash
# Setup Mac scripts and sync
cd mac
./setup.sh

# Test the integration
./add_task.py "Test task from command line"
./sync_obsidian.py
```

### 4. Alfred Workflow Setup

Follow instructions in `mac/alfred_workflow.md`:
1. Create new Alfred workflow
2. Add keyword trigger: `task`
3. Connect to Python script
4. Test: `Cmd+Space` → `task Buy milk`

### 5. Optional: Additional Triggers

#### WhatsApp Integration
```bash
cd triggers/whatsapp
# Follow setup.md instructions
# Deploy webhook Lambda
# Configure Twilio
```

#### Email Integration
```bash
cd triggers/email
# Deploy email handler Lambda
# Configure SES rules
```

#### Web Form
```bash
cd triggers/web
# Host web_form.html on S3 or web server
# Update API endpoint in HTML
```

## Testing

### Quick Test
```bash
cd tests
./manual_test.py
```

### Full Integration Test
```bash
cd tests
./test_integration.py
```

### Manual Testing
1. **Mac**: `task Buy groceries` in Alfred
2. **API**: Use Postman/curl to test endpoint
3. **Obsidian**: Check vault for new tasks
4. **Sync**: Run sync script manually

## Troubleshooting

### Common Issues

**API Gateway 403 Error**
- Check IAM permissions
- Verify API Gateway deployment
- Test Lambda function directly

**Obsidian Sync Not Working**
- Check vault path in .env
- Verify AWS credentials
- Run sync script with verbose output

**Alfred Not Responding**
- Check script paths in workflow
- Test script directly in terminal
- Verify .env file location

**Bedrock Access Denied**
- Enable Bedrock in AWS console
- Check IAM permissions
- Verify model access (Claude Haiku)

### Debug Commands

```bash
# Test AWS credentials
aws sts get-caller-identity

# Test Lambda function
aws lambda invoke --function-name task-organizer --payload '{"body":"{\"task\":\"test\",\"source\":\"cli\"}"}' response.json

# Test DynamoDB access
aws dynamodb scan --table-name tasks --max-items 5

# Check Obsidian vault
ls -la "$OBSIDIAN_VAULT_PATH/Tasks"
```

## Usage Examples

### Mac (Alfred)
- `task Buy groceries for dinner party`
- `task Call dentist tomorrow at 2pm`
- `task Finish project report by Friday`

### WhatsApp
Send message to Twilio number:
- "Buy milk and bread"
- "Schedule team meeting"

### Email
Send email with subject:
- `[task] Review quarterly budget`
- `[task] Book flight to conference`

### Web Form
Visit hosted web form and enter tasks naturally.

## Maintenance

### Regular Tasks
- Monitor AWS costs
- Check Obsidian vault organization
- Update Bedrock prompts if needed
- Review and clean up old tasks

### Updates
- Pull latest code changes
- Redeploy Lambda functions
- Update Alfred workflow if needed

## Support

Check logs:
- **Lambda**: CloudWatch Logs
- **Mac Scripts**: Terminal output
- **Alfred**: Alfred debugger

For issues, check the troubleshooting section or create an issue in the repository.