# src/task_manager.py
import json
import os
from datetime import datetime
from rich.console import Console

console = Console()
DATA_FILE = "data/tasks.json"

def ensure_data_dir():
    """Ensure data directory exists"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def load_tasks():
    """Load tasks from JSON file"""
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]❌ Error loading tasks: {e}[/red]")
        return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    ensure_data_dir()
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(tasks, f, indent=2)
    except Exception as e:
        console.print(f"[red]❌ Error saving tasks: {e}[/red]")

def add_task(task_text):
    """Add a new task"""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "text": task_text,
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)
    console.print(f"[green]✅ Task added: {task_text}[/green]")

def complete_task(task_id):
    """Mark task as completed"""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            console.print(f"[green]✅ Task {task_id} completed[/green]")
            return
    console.print(f"[yellow]⚠️ Task {task_id} not found[/yellow]")

def show_tasks():
    """Display all tasks"""
    tasks = load_tasks()
    if not tasks:
        console.print("[yellow]📋 No tasks found.[/yellow]")
        return

    console.print("\n[bold cyan]📋 Tasks:[/bold cyan]")
    for t in tasks:
        status = "✅" if t["completed"] else "❌"
        created = datetime.fromisoformat(t["created_at"]).strftime("%Y-%m-%d %H:%M")
        console.print(f"  {status} [{t['id']}] {t['text']} [dim]({created})[/dim]")
