import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest

from tasks import search_tasks, sort_tasks_by_due_date, mark_all_tasks_completed

#Search by Keyword
def test_search_by_keyword():
    tasks = [
        {"title": "Complete Homework 4", "description": "HW4 for CS1234"},
        {"title": "Finish Art Project", "description": "Finish painting for homework"},
        {"title": "Call Wife", "description": "Tell her I love her"} 
    ]
    result = search_tasks(tasks, "homework")
    assert len(result) == 2
    assert result[0]["title"] == "Complete Homework 4"

#Sort by Due Date
def test_sort_tasks_by_due_date_ascending():
    tasks = [
        {"title": "Task A", "due_date": "2025-04-30"},
        {"title": "Task B", "due_date": "2025-04-28"},
    ]
    result = sort_tasks_by_due_date(tasks, ascending=True)
    assert result[0]["title"] == "Task B"

def test_sort_tasks_by_due_date_descending():
    tasks = [
        {"title": "Task A", "due_date": "2025-04-30"},
        {"title": "Task B", "due_date": "2025-04-28"},
    ]
    result = sort_tasks_by_due_date(tasks, ascending=False)
    assert result[0]["title"] == "Task A"

#Mark All as Complete
def test_mark_all_tasks_completed():
    tasks = [
        {"title": "A", "completed": False},
        {"title": "B", "completed": False},
    ]
    updated_tasks = mark_all_tasks_completed(tasks)
    assert all(task["completed"] for task in updated_tasks)