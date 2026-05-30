import yaml
import os
from pathlib import Path
from datetime import datetime

class BenchmarkLoader:
    def __init__(self):
        self.tasks_dir = Path("tasks")
        self.tasks = []
        self.load_all_tasks()
    
    def load_all_tasks(self):
        """Load all tasks from the tasks folder"""
        if not self.tasks_dir.exists():
            print("❌ Tasks folder not found!")
            return
        
        for file in sorted(self.tasks_dir.glob("*.yaml")):
            try:
                with open(file, 'r') as f:
                    task = yaml.safe_load(f)
                    task['filename'] = file.name
                    self.tasks.append(task)
                    print(f"✅ Loaded: {task['id']} - {task['title']}")
            except Exception as e:
                print(f"❌ Error loading {file}: {e}")
    
    def list_tasks(self):
        """Show all available tasks"""
        print(f"\n📋 Benchmark Tasks Loaded: {len(self.tasks)}\n")
        for i, task in enumerate(self.tasks, 1):
            print(f"{i:2d}. [{task['difficulty'].upper()}] {task['title']}")
            print(f"    Category: {task['category']} | ID: {task['id']}")
            print("-" * 60)
    
    def get_task(self, task_id):
        """Get a specific task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

# Quick test
if __name__ == "__main__":
    loader = BenchmarkLoader()
    loader.list_tasks()
