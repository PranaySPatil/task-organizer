"""
Email handler for SES integration
Deploy this as a Lambda function triggered by SES
"""

import json
import requests
import os
import email
from email.mime.text import MIMEText

def lambda_handler(event, context):
    """Handle incoming emails from SES"""
    try:
        # Parse SES event
        for record in event['Records']:
            if record['eventSource'] == 'aws:ses':
                handle_ses_email(record['ses'])
        
        return {'statusCode': 200, 'body': 'Processed'}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500, 'body': str(e)}

def handle_ses_email(ses_data):
    """Process SES email data"""
    mail = ses_data['mail']
    
    # Extract email details
    subject = mail['commonHeaders']['subject']
    sender = mail['commonHeaders']['from'][0]
    
    # Get message content (simplified - in real implementation, 
    # you'd parse the full email content from S3)
    task_content = f"{subject}"
    
    # Only process emails with specific subject prefix
    if not subject.lower().startswith('[task]'):
        print(f"Ignoring email without [task] prefix: {subject}")
        return
    
    # Remove [task] prefix
    task_content = subject[6:].strip()
    
    # Forward to main task organizer
    task_api_endpoint = os.environ['TASK_API_ENDPOINT']
    
    payload = {
        'task': task_content,
        'source': f'email:{sender}'
    }
    
    response = requests.post(task_api_endpoint, json=payload, timeout=10)
    
    if response.status_code == 200:
        result = response.json()
        organized_task = result.get('organized_task', {})
        
        # Send confirmation email back
        send_confirmation_email(sender, organized_task)
        print(f"✅ Task organized from email: {task_content}")
    else:
        print(f"❌ Failed to organize task from email: {response.text}")

def send_confirmation_email(recipient, organized_task):
    """Send confirmation email using SES"""
    import boto3
    
    ses = boto3.client('ses')
    
    subject = f"✅ Task Organized: {organized_task.get('category', 'Unknown')}"
    
    body = f"""Your task has been organized!

Task: {organized_task.get('task', 'Unknown')}
Category: {organized_task.get('category', 'Unknown')}
Priority: {organized_task.get('priority', 'medium')}
Estimated Time: {organized_task.get('estimated_time', 30)} minutes

The task has been added to your Obsidian vault and will sync automatically.

---
Task Organizer System
"""
    
    try:
        ses.send_email(
            Source='tasks@yourdomain.com',  # Replace with your verified SES email
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        print(f"✅ Confirmation email sent to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send confirmation email: {str(e)}")