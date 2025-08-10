#!/bin/bash

# Setup Mac integration for task organizer

set -e

echo "🍎 Setting up Mac integration..."

# Make scripts executable
chmod +x add_task.py
chmod +x sync_obsidian.py

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install requests boto3

# Create Obsidian vault structure if it doesn't exist
VAULT_PATH=$(grep OBSIDIAN_VAULT_PATH ../.env | cut -d'=' -f2)
if [ ! -z "$VAULT_PATH" ]; then
    echo "📁 Creating Obsidian vault structure..."
    mkdir -p "$VAULT_PATH/Tasks"/{Work,Personal,Projects,Health,Shopping,Learning}
    echo "Created task folders in: $VAULT_PATH/Tasks"
fi

# Setup cron job for automatic sync
echo "⏰ Setting up automatic sync (every 5 minutes)..."
SCRIPT_PATH="$(pwd)/sync_obsidian.py"
CRON_JOB="*/5 * * * * /Users/prantil/task-organizer/venv/bin/python3 $SCRIPT_PATH"

# Add to crontab if not already present
(crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_JOB") | crontab -

echo "✅ Mac setup complete!"
echo ""
echo "Next steps:"
echo "1. Test task addition: ./add_task.py 'Test task from Mac'"
echo "2. Test sync: ./sync_obsidian.py"
echo "3. Setup Alfred workflow (see alfred_workflow.md)"
echo ""
echo "Alfred keyword will be: task <your task>"