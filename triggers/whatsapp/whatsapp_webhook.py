"""
WhatsApp webhook handler for Twilio
Deploy this as a separate Lambda function
"""

import json
import requests
import os
from urllib.parse import parse_qs

def lambda_handler(event, context):
    """Handle WhatsApp messages from Twilio"""
    try:
        # Parse Twilio webhook data
        body = event.get('body', '')
        if event.get('isBase64Encoded'):
            import base64
            body = base64.b64decode(body).decode('utf-8')
        
        # Parse form data
        data = parse_qs(body)
        
        # Extract message details
        message_body = data.get('Body', [''])[0]
        from_number = data.get('From', [''])[0]
        
        if not message_body:
            return create_response("No message received")
        
        # Forward to main task organizer
        task_api_endpoint = os.environ['TASK_API_ENDPOINT']
        
        payload = {
            'task': message_body,
            'source': f'whatsapp:{from_number}'
        }
        
        response = requests.post(task_api_endpoint, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            organized_task = result.get('organized_task', {})
            
            # Send confirmation back to WhatsApp
            confirmation = f"✅ Task organized!\n"
            confirmation += f"Category: {organized_task.get('category', 'Unknown')}\n"
            confirmation += f"Priority: {organized_task.get('priority', 'medium')}\n"
            confirmation += f"Est. time: {organized_task.get('estimated_time', 30)} min"
            
            return create_twilio_response(confirmation)
        else:
            return create_twilio_response("❌ Failed to organize task")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_twilio_response("❌ Error processing task")

def create_response(message):
    """Create standard HTTP response"""
    return {
        'statusCode': 200,
        'body': json.dumps({'message': message})
    }

def create_twilio_response(message):
    """Create Twilio TwiML response"""
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>"""
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/xml'},
        'body': twiml
    }