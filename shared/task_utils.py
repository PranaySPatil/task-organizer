"""
Shared utilities for task organization system
"""

import json
import boto3
from datetime import datetime
from typing import Dict, List, Optional

class TaskOrganizer:
    """Shared task organization utilities"""
    
    def __init__(self, region='us-east-1'):
        self.bedrock = boto3.client('bedrock-runtime', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.table = self.dynamodb.Table('tasks')
    
    def organize_task(self, task_text: str) -> Dict:
        """Organize task using Bedrock AI"""
        prompt = f"""Analyze this task and return ONLY a JSON object with these fields:
- "task": the original task text
- "category": best category (Work, Personal, Projects, Health, Shopping, Learning)
- "priority": high, medium, or low
- "estimated_time": estimated minutes as integer
- "tags": array of relevant tags

Task: {task_text}

Return only valid JSON, no other text."""
        
        try:
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-haiku-20240307-v1:0',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 300
                })
            )
            
            result = json.loads(response['body'].read())
            organized_task = json.loads(result['content'][0]['text'])
            
            # Ensure required fields
            organized_task.setdefault('task', task_text)
            organized_task.setdefault('category', 'Personal')
            organized_task.setdefault('priority', 'medium')
            organized_task.setdefault('estimated_time', 30)
            organized_task.setdefault('tags', [])
            
            return organized_task
            
        except Exception as e:
            print(f"Bedrock error: {str(e)}")
            return self._fallback_organization(task_text)
    
    def _fallback_organization(self, task_text: str) -> Dict:
        """Fallback organization when Bedrock fails"""
        # Simple keyword-based categorization
        task_lower = task_text.lower()
        
        if any(word in task_lower for word in ['buy', 'shop', 'grocery', 'store']):
            category = 'Shopping'
        elif any(word in task_lower for word in ['work', 'meeting', 'project', 'deadline']):
            category = 'Work'
        elif any(word in task_lower for word in ['doctor', 'health', 'exercise', 'gym']):
            category = 'Health'
        elif any(word in task_lower for word in ['learn', 'study', 'read', 'course']):
            category = 'Learning'
        else:
            category = 'Personal'
        
        # Simple priority detection
        if any(word in task_lower for word in ['urgent', 'asap', 'immediately', 'critical']):
            priority = 'high'
        elif any(word in task_lower for word in ['later', 'someday', 'maybe']):
            priority = 'low'
        else:
            priority = 'medium'
        
        return {
            'task': task_text,
            'category': category,
            'priority': priority,
            'estimated_time': 30,
            'tags': []
        }
    
    def store_task(self, organized_task: Dict, source: str) -> str:
        """Store task in DynamoDB"""
        import uuid
        
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
        
        self.table.put_item(Item=item)
        return task_id
    
    def get_unsynced_tasks(self) -> List[Dict]:
        """Get tasks that haven't been synced to Obsidian"""
        response = self.table.scan(
            FilterExpression='synced_to_obsidian = :val',
            ExpressionAttributeValues={':val': False}
        )
        return response['Items']
    
    def mark_task_synced(self, task_id: str):
        """Mark task as synced to Obsidian"""
        self.table.update_item(
            Key={'id': task_id},
            UpdateExpression='SET synced_to_obsidian = :val',
            ExpressionAttributeValues={':val': True}
        )

def validate_task_input(task_text: str) -> bool:
    """Validate task input"""
    if not task_text or not task_text.strip():
        return False
    if len(task_text.strip()) < 3:
        return False
    return True

def format_task_for_obsidian(task: Dict) -> str:
    """Format task as Obsidian markdown"""
    tags_str = " ".join([f"#{tag}" for tag in task.get('tags', [])])
    
    content = f"""# {task['task']}

**Priority:** {task['priority']}
**Category:** {task['category']}
**Source:** {task['source']}
**Estimated Time:** {task.get('estimated_time', 30)} minutes
**Added:** {task['timestamp']}

{tags_str}

## Notes
- [ ] {task['task']}

## Details
<!-- Add additional notes, links, or details here -->

---
*Auto-generated from task organizer - ID: {task['id']}*
"""
    return content