import json
import boto3
import uuid
from datetime import datetime

def lambda_handler(event, context):
    """Main Lambda handler for task organization"""
    try:
        # Parse request
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        new_task = body['task']
        source = body.get('source', 'unknown')
        
        # Organize with Bedrock
        organized_task = organize_with_bedrock(new_task)
        
        # Store in DynamoDB
        task_id = store_task(organized_task, source)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'id': task_id,
                'message': 'Task organized and stored',
                'organized_task': organized_task
            })
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def organize_with_bedrock(task):
    """Use Bedrock to organize and categorize the task"""
    bedrock = boto3.client('bedrock-runtime')
    
    prompt = f"""Analyze this task and return ONLY a JSON object with these fields:
- "task": the original task text
- "category": best category (Work, Personal, Projects, Health, Shopping, Learning)
- "priority": high, medium, or low
- "estimated_time": estimated minutes as integer
- "tags": array of relevant tags

Task: {task}

Return only valid JSON, no other text."""
    
    try:
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 300
            })
        )
        
        result = json.loads(response['body'].read())
        organized_task = json.loads(result['content'][0]['text'])
        
        # Ensure required fields exist
        organized_task.setdefault('task', task)
        organized_task.setdefault('category', 'Personal')
        organized_task.setdefault('priority', 'medium')
        organized_task.setdefault('estimated_time', 30)
        organized_task.setdefault('tags', [])
        
        return organized_task
        
    except Exception as e:
        print(f"Bedrock error: {str(e)}")
        # Fallback organization
        return {
            'task': task,
            'category': 'Personal',
            'priority': 'medium',
            'estimated_time': 30,
            'tags': []
        }

def store_task(organized_task, source):
    """Store task in DynamoDB"""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('tasks')
    
    task_id = str(uuid.uuid4())
    
    item = {
        'id': task_id,
        'task': organized_task['task'],
        'category': organized_task['category'],
        'priority': organized_task['priority'],
        'estimated_time': organized_task['estimated_time'],
        'tags': organized_task['tags'],
        'source': source,
        'timestamp': datetime.now().isoformat(),
        'synced_to_obsidian': False,
        'completed': False
    }
    
    table.put_item(Item=item)
    return task_id