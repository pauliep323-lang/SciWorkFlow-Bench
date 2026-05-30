import yaml
from pathlib import Path
from datetime import datetime
from loader import BenchmarkLoader

class TaskRunner:
    def __init__(self):
        self.loader = BenchmarkLoader()
    
    def run_task(self):
        self.loader.list_tasks()
        choice = input("\nEnter task number to run (or 'q' to quit): ")
        if choice.lower() == 'q':
            return False
        
        try:
            task = self.loader.tasks[int(choice)-1]
        except:
            print("Invalid choice.")
            return True
        
        print(f"\n{'='*80}")
        print(f"🚀 RUNNING TASK: {task['title']}")
        print(f"Difficulty: {task['difficulty'].upper()} | Category: {task['category']}")
        print(f"{'='*80}\n")
        print(task['description'])
        
        if task.get('hints'):
            if input("\nShow hints? (y/n): ").lower() == 'y':
                print("\n💡 Hints:")
                for hint in task['hints']:
                    print(f"   • {hint}")
        
        print("\n" + "="*80)
        print("Type your answer below. When finished, type 'END' on a new line and press Enter.")
        print("="*80)
        
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        
        answer = "\n".join(lines)
        print("\n✅ Answer submitted successfully!")
        print("-" * 60)
        print(answer)
        print("-" * 60)
        return True

if __name__ == "__main__":
    runner = TaskRunner()
    while runner.run_task():
        pass
    print("Goodbye!")
