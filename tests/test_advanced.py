import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest
from tasks import load_tasks, filter_tasks_by_priority, save_tasks
import json

# Mock the load_tasks function
@pytest.fixture
def mock_load_tasks(monkeypatch):
    def mock_return_value(file_path):
        return [
            {"id": 1, "title": "Mocked Task", "priority": "High", "category": "Work", "due_date": "2025-04-30", "completed": False}
        ]
    monkeypatch.setattr("test_advanced.load_tasks", mock_return_value)
    return mock_return_value

# Parameterized test for filter tasks by priority
@pytest.mark.parametrize("priority, expected_length", [
    ("High", 1),
    ("Medium", 0),
    ("Low", 1)
])
def test_filter_tasks_by_priority(priority, expected_length):
    tasks = [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "Work", "due_date": "2025-04-30", "completed": False},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "due_date": "2025-04-28", "completed": False}
    ]
    result = filter_tasks_by_priority(tasks, priority)
    assert len(result) == expected_length

# Test the load_tasks with mocking
def test_load_tasks(mock_load_tasks):
    tasks = load_tasks("mock_file.json")
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Mocked Task"

# Test save_tasks function
def test_save_tasks():
    tasks = [
        {"id": 1, "title": "Save this task", "priority": "High", "category": "Work", "due_date": "2025-04-30", "completed": False}
    ]
    save_tasks(tasks, "mock_save_tasks.json")
    with open("mock_save_tasks.json", "r") as f:
        saved_tasks = json.load(f)
    assert saved_tasks == tasks
