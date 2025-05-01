import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
import json
from tasks import filter_tasks_by_completion, filter_tasks_by_category, filter_tasks_by_priority, save_tasks, load_tasks

def test_load_tasks():
    test_file_path = "test_tasks.json"

    tasks = load_tasks(test_file_path)
    assert isinstance(tasks, list)

def test_save_tasks():

    tasks = [
        {"id": 1, "title": "Test Task", "description": "A task for testing", "priority": "High", "category": "Work", "due_date": "2025-04-30", "completed": False, "created_at": "2025-04-25 12:00:00"}
    ]
    test_file_path = "test_save_tasks.json"

    save_tasks(tasks, test_file_path)
    assert os.path.exists(test_file_path)

    with open(test_file_path, "r") as f:
        loaded_tasks = json.load(f)
    
    assert loaded_tasks == tasks
    os.remove(test_file_path)

def test_filter_tasks_by_priority():
    tasks = [
        {"id": 1, "title": "High priority task", "priority": "High", "category": "Work", "due_date": "2025-04-30", "completed": False},
        {"id": 2, "title": "Low priority task", "priority": "Low", "category": "Personal", "due_date": "2025-04-28", "completed": False}
    ]
    
    result = filter_tasks_by_priority(tasks, "High")
    assert len(result) == 1
    assert result[0]["priority"] == "High"

def test_filter_tasks_by_category():
    tasks = [
        {"id": 1, "title": "Work task", "category": "Work", "due_date": "2025-04-30", "completed": False},
        {"id": 2, "title": "Personal task", "category": "Personal", "due_date": "2025-04-28", "completed": False}
    ]
    
    result = filter_tasks_by_category(tasks, "Work")
    assert len(result) == 1
    assert result[0]["category"] == "Work"

def test_task_completion():
    tasks = [
        {"id": 1, "title": "Complete assignment", "completed": False},
        {"id": 2, "title": "Buy groceries", "completed": True}
    ]
    
    result = filter_tasks_by_completion(tasks, completed=True)
    assert len(result) == 1
    assert result[0]["completed"] is True