# Task Organizer Project

AI-powered task organization system with multiple input sources and Obsidian storage.

## Architecture
- **AWS Lambda**: AI task organization using Bedrock
- **DynamoDB**: Cloud task storage
- **Mac Script**: Local Alfred integration and Obsidian sync
- **Multiple Triggers**: Mac, WhatsApp, Email, Web

## Quick Start
1. Deploy AWS infrastructure: `cd aws && terraform apply`
2. Set up Mac integration: `cd mac && ./setup.sh`
3. Configure triggers: See individual trigger folders

## Project Structure
```
task-organizer/
├── aws/                 # AWS Lambda + Infrastructure
├── mac/                 # Mac Alfred integration + Obsidian sync
├── triggers/            # Various input sources
│   ├── whatsapp/
│   ├── email/
│   └── web/
├── shared/              # Common utilities
└── tests/               # Test scripts
```

## Environment Variables
Copy `.env.example` to `.env` and fill in your values:
- AWS credentials
- API endpoints
- Obsidian vault path