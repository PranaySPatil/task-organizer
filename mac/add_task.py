#!/Users/prantil/task-organizer/venv/bin/python
"""
Mac script for adding tasks via Alfred
Sends task to AWS Lambda for organization
"""

import requests
import sys
import os
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

def send_task_to_aws(task_input):
    """Send task to AWS Lambda for organization"""
    load_env()
    
    api_endpoint = os.getenv('TASK_API_ENDPOINT')
    if not api_endpoint:
        print("❌ TASK_API_ENDPOINT not set in .env file")
        return
    
    payload = {
        'task': task_input,
        'source': 'mac'
    }
    
    try:
        response = requests.post(
            api_endpoint,
            json=payload,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Task organized: {result.get('organized_task', {}).get('category', 'Unknown')}")
            print(f"   Priority: {result.get('organized_task', {}).get('priority', 'medium')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send task: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

def main():
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        send_task_to_aws(task)
    else:
        print("Usage: add_task.py <task description>")
        print("Example: add_task.py 'Buy groceries for dinner party'")

if __name__ == "__main__":
    main()