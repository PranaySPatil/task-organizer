#!/usr/bin/env python3
"""
Sync tasks from DynamoDB to Obsidian vault
Run this script periodically to keep Obsidian updated
"""

import boto3
import os
from datetime import datetime
from pathlib import Path

def load_env():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def sync_to_obsidian():
    """Sync unsynced tasks from DynamoDB to Obsidian"""
    load_env()
    
    vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
    if not vault_path:
        print("❌ OBSIDIAN_VAULT_PATH not set in .env file")
        return
    
    vault_path = Path(vault_path)
    if not vault_path.exists():
        print(f"❌ Obsidian vault not found at: {vault_path}")
        return
    
    try:
        # Connect to DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('tasks')
        
        # Get unsynced tasks
        response = table.scan(
            FilterExpression='synced_to_obsidian = :val',
            ExpressionAttributeValues={':val': False}
        )
        
        tasks_synced = 0
        
        for item in response['Items']:
            write_task_to_obsidian(item, vault_path)
            
            # Mark as synced
            table.update_item(
                Key={'id': item['id']},
                UpdateExpression='SET synced_to_obsidian = :val',
                ExpressionAttributeValues={':val': True}
            )
            
            tasks_synced += 1
        
        if tasks_synced > 0:
            print(f"✅ Synced {tasks_synced} tasks to Obsidian")
        else:
            print("📝 No new tasks to sync")
            
    except Exception as e:
        print(f"❌ Sync failed: {str(e)}")

def write_task_to_obsidian(task, vault_path):
    """Write a single task to Obsidian vault"""
    # Create category folder
    category_path = vault_path / 'Tasks' / task['category']
    category_path.mkdir(parents=True, exist_ok=True)
    
    # Create filename
    date_str = datetime.now().strftime('%Y-%m-%d')
    task_id_short = task['id'][:8]
    safe_task = "".join(c for c in task['task'][:30] if c.isalnum() or c in (' ', '-', '_')).strip()
    filename = f"{task['priority']}-{date_str}-{safe_task}-{task_id_short}.md"
    
    file_path = category_path / filename
    
    # Create markdown content
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
    
    # Write to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📝 Added: {task['task'][:50]}...")

def main():
    sync_to_obsidian()

if __name__ == "__main__":
    main()