#!/usr/bin/env python3
"""
Manual testing script for quick validation
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def test_bedrock_organization():
    """Test Bedrock task organization locally"""
    try:
        from shared.task_utils import TaskOrganizer
        
        organizer = TaskOrganizer()
        
        test_tasks = [
            "Buy groceries for dinner party",
            "Call dentist to schedule appointment",
            "Finish quarterly report by Friday",
            "Go for a run in the morning",
            "Learn Python decorators"
        ]
        
        print("🧪 Testing Bedrock task organization...\n")
        
        for task in test_tasks:
            print(f"Task: {task}")
            organized = organizer.organize_task(task)
            print(f"  Category: {organized['category']}")
            print(f"  Priority: {organized['priority']}")
            print(f"  Time: {organized['estimated_time']} min")
            print(f"  Tags: {organized['tags']}")
            print()
        
        print("✅ Bedrock organization test completed")
        
    except Exception as e:
        print(f"❌ Bedrock test failed: {str(e)}")

def test_obsidian_formatting():
    """Test Obsidian markdown formatting"""
    try:
        from shared.task_utils import format_task_for_obsidian
        
        sample_task = {
            'id': 'test-123',
            'task': 'Buy groceries for dinner party',
            'category': 'Shopping',
            'priority': 'high',
            'estimated_time': 45,
            'tags': ['shopping', 'food', 'party'],
            'source': 'test',
            'timestamp': '2024-01-15T10:30:00'
        }
        
        print("🧪 Testing Obsidian formatting...\n")
        
        markdown = format_task_for_obsidian(sample_task)
        print(markdown)
        
        print("✅ Obsidian formatting test completed")
        
    except Exception as e:
        print(f"❌ Obsidian formatting test failed: {str(e)}")

def interactive_test():
    """Interactive testing mode"""
    print("🎮 Interactive Task Organizer Test")
    print("Enter tasks to see how they get organized (type 'quit' to exit)\n")
    
    try:
        from shared.task_utils import TaskOrganizer
        organizer = TaskOrganizer()
        
        while True:
            task = input("Enter task: ").strip()
            
            if task.lower() in ['quit', 'exit', 'q']:
                break
            
            if not task:
                continue
            
            try:
                organized = organizer.organize_task(task)
                print(f"  📂 Category: {organized['category']}")
                print(f"  ⚡ Priority: {organized['priority']}")
                print(f"  ⏱️  Time: {organized['estimated_time']} min")
                print(f"  🏷️  Tags: {', '.join(organized['tags']) if organized['tags'] else 'None'}")
                print()
            except Exception as e:
                print(f"  ❌ Error: {str(e)}\n")
        
        print("👋 Goodbye!")
        
    except Exception as e:
        print(f"❌ Interactive test failed: {str(e)}")

def main():
    """Main test menu"""
    print("🧪 Task Organizer Manual Tests\n")
    print("1. Test Bedrock organization")
    print("2. Test Obsidian formatting")
    print("3. Interactive testing")
    print("4. Run all tests")
    
    choice = input("\nSelect test (1-4): ").strip()
    
    if choice == '1':
        test_bedrock_organization()
    elif choice == '2':
        test_obsidian_formatting()
    elif choice == '3':
        interactive_test()
    elif choice == '4':
        test_bedrock_organization()
        print("\n" + "-"*50 + "\n")
        test_obsidian_formatting()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()