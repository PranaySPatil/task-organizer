#!/usr/bin/env python3
"""
Integration tests for task organizer system
"""

import requests
import json
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

def load_env():
    """Load environment variables"""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def test_api_endpoint():
    """Test the main API endpoint"""
    load_env()
    
    api_endpoint = os.getenv('TASK_API_ENDPOINT')
    if not api_endpoint:
        print("❌ TASK_API_ENDPOINT not set")
        return False
    
    test_task = "Test task from integration test"
    payload = {
        'task': test_task,
        'source': 'test'
    }
    
    try:
        print(f"🧪 Testing API endpoint: {api_endpoint}")
        response = requests.post(api_endpoint, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API test passed")
            print(f"   Task ID: {result.get('id', 'Unknown')}")
            print(f"   Category: {result.get('organized_task', {}).get('category', 'Unknown')}")
            print(f"   Priority: {result.get('organized_task', {}).get('priority', 'Unknown')}")
            return True
        else:
            print(f"❌ API test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test error: {str(e)}")
        return False

def test_mac_script():
    """Test Mac add_task script"""
    script_path = Path(__file__).parent.parent / 'mac' / 'add_task.py'
    
    if not script_path.exists():
        print("❌ Mac script not found")
        return False
    
    try:
        import subprocess
        print("🧪 Testing Mac script...")
        
        result = subprocess.run([
            'python3', str(script_path), 'Test task from Mac script'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Mac script test passed")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print("❌ Mac script test failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Mac script test error: {str(e)}")
        return False

def test_obsidian_sync():
    """Test Obsidian sync script"""
    script_path = Path(__file__).parent.parent / 'mac' / 'sync_obsidian.py'
    
    if not script_path.exists():
        print("❌ Obsidian sync script not found")
        return False
    
    try:
        import subprocess
        print("🧪 Testing Obsidian sync...")
        
        result = subprocess.run([
            'python3', str(script_path)
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Obsidian sync test passed")
            print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print("❌ Obsidian sync test failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Obsidian sync test error: {str(e)}")
        return False

def test_shared_utils():
    """Test shared utilities"""
    try:
        from shared.task_utils import TaskOrganizer, validate_task_input
        
        print("🧪 Testing shared utilities...")
        
        # Test validation
        assert validate_task_input("Valid task") == True
        assert validate_task_input("") == False
        assert validate_task_input("ab") == False
        
        print("✅ Shared utilities test passed")
        return True
        
    except Exception as e:
        print(f"❌ Shared utilities test error: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print("🚀 Running Task Organizer Integration Tests\n")
    
    tests = [
        ("Shared Utilities", test_shared_utils),
        ("API Endpoint", test_api_endpoint),
        ("Mac Script", test_mac_script),
        ("Obsidian Sync", test_obsidian_sync),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        success = test_func()
        results.append((test_name, success))
    
    print("\n" + "="*50)
    print("TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if success:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed. Check configuration and try again.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)