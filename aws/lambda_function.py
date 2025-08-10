import json
import boto3
import uuid
from datetime import datetime

def lambda_handler(event, context):
    """Main Lambda handler for task organization"""
    try:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        new_task = body['task']
        source = body.get('source', 'unknown')
        
        organized_task = organize_with_bedrock(new_task)
        task_id = store_task(organized_task, source)
        
        # Find and store task links
        find_and_store_links(task_id, organized_task)
        
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

def find_and_store_links(new_task_id, new_task):
    """Find links between new task and existing tasks"""
    dynamodb = boto3.resource('dynamodb')
    tasks_table = dynamodb.Table('tasks')
    links_table = dynamodb.Table('task-links')
    
    # Get existing tasks
    response = tasks_table.scan()
    existing_tasks = [item for item in response['Items'] if item['id'] != new_task_id]
    
    if not existing_tasks:
        return
    
    # Use Bedrock to find links
    bedrock = boto3.client('bedrock-runtime')
    
    existing_tasks_text = "\n".join([
        f"ID: {task['id']}, Task: {task['task']}, Category: {task['category']}"
        for task in existing_tasks
    ])
    
    prompt = f"""Analyze if this new task has relationships with existing tasks.

New Task: {new_task['task']} (Category: {new_task['category']})

Existing Tasks:
{existing_tasks_text}

Return ONLY a JSON array of task IDs that are related to the new task. Consider:
- Similar topics or projects
- Dependencies (one task blocks another)
- Sequential tasks in same category
- Related shopping items
- Connected work projects

Return empty array [] if no relationships found.
Example: ["task-id-1", "task-id-2"]"""
    
    print(f"Prompt for link finding: {prompt}")

    try:
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 200
            })
        )
        
        result = json.loads(response['body'].read())
        print(f"Link finding result: {result}")
        linked_task_ids = json.loads(result['content'][0]['text'])
        
        # Store links
        for linked_id in linked_task_ids:
            links_table.put_item(Item={
                'source_task_id': new_task_id,
                'target_task_id': linked_id,
                'link_type': 'related',
                'created_at': datetime.now().isoformat()
            })
            
    except Exception as e:
        print(f"Link finding error: {str(e)}")

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