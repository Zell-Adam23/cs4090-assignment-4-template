import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest

from hypothesis import given
from hypothesis.strategies import lists, sampled_from, text, booleans, dates, integers, fixed_dictionaries
from tasks import filter_tasks_by_priority, filter_tasks_by_completion, search_tasks, get_overdue_tasks, filter_tasks_by_category
from datetime import datetime, timedelta

task_strategy = fixed_dictionaries({
    "id": integers(min_value=1, max_value=1000),
    "title": text(min_size=1, max_size=20),
    "description": text(min_size=1, max_size=20),
    "priority": sampled_from(["High", "Medium", "Low"]),
    "category": sampled_from(["School", "Work", "Personal", "Other"]),
    "due_date": dates().map(lambda d: d.strftime("%Y-%m-%d")),
    "completed": booleans()
})

@given(
    tasks=lists(task_strategy, min_size=5, max_size=20),
    target_priority=sampled_from(["High", "Medium", "Low"])
)

def test_filter_tasks_by_priority_property(tasks, target_priority):
    filtered = filter_tasks_by_priority(tasks, target_priority)
    assert all(task["priority"] == target_priority for task in filtered)

@given(
    tasks=lists(task_strategy, min_size=5, max_size=20),
    completed=booleans()
)

def test_filter_tasks_by_completion_property(tasks, completed):
    result = filter_tasks_by_completion(tasks, completed)
    assert all(task["completed"] == completed for task in result)

@given(
    tasks=lists(task_strategy, min_size=5, max_size=20),
    query=text(min_size=1, max_size=20)
)

def test_search_tasks_property(tasks, query):
    result = search_tasks(tasks, query)
    for task in result:
        in_title = query.lower() in task["title"].lower()
        in_description = query.lower() in task["description"].lower()
        assert in_title or in_description

@given(
    tasks=lists(task_strategy, min_size=5, max_size=20)
)

def test_get_overdue_tasks_property(tasks):
    today = datetime.now().strftime("%Y-%m-%d")
    result = get_overdue_tasks(tasks)
    for task in result:
        assert task["due_date"] < today
        assert not task["completed"]

@given(
    tasks=lists(task_strategy, min_size=5, max_size=20),
    category=sampled_from(["School", "Work", "Personal", "Other"])
)

def test_filter_tasks_by_category_property(tasks, category):
    result = filter_tasks_by_category(tasks, category)
    assert all(task["category"] == category for task in result)