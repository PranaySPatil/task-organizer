# Alfred Workflow Setup

## Create Alfred Workflow

1. Open Alfred Preferences
2. Go to **Workflows** tab
3. Click **+** → **Blank Workflow**
4. Name: "Task Organizer"
5. Description: "AI-powered task organization"

## Add Keyword Input

1. Click **+** → **Inputs** → **Keyword**
2. Configure:
   - **Keyword**: `task`
   - **With Space**: ✅ (checked)
   - **Argument**: Required
   - **Title**: Add Task
   - **Subtext**: Add task: {query}

## Add Run Script Action

1. Click **+** → **Actions** → **Run Script**
2. Configure:
   - **Language**: `/usr/bin/python3`
   - **Script**: 
   ```python
   import sys
   import subprocess
      
   query = sys.argv[1] if len(sys.argv) > 1 else ""
   python_env_path = "/Users/prantil/task-organizer/venv/bin/python3"
   script_path = "/Users/prantil/task-organizer/mac/add_task.py"
      
   result = subprocess.run([python_env_path, script_path, query], capture_output=True, text=True)
      
   print(result.stdout if result.stdout else result.stderr)
   ```

## Add Post Notification
1. In Alfred workflow, click + → Outputs → Post Notification
2. Configure notification:
   - **Title**: Task Result
   - **Text**: {query}

## Connect Components

1. Drag from **Keyword** output to **Run Script** input
2. Connect the Run Script output to Post Notification input
3. Save workflow

## Test

1. Press `Cmd + Space` (Alfred hotkey)
2. Type: `task Buy groceries for dinner`
3. Press Enter
4. Should see confirmation message

## Troubleshooting

- Ensure script paths are correct
- Check .env file is properly configured
- Verify AWS credentials are set
- Test script directly: `./add_task.py "test task"`