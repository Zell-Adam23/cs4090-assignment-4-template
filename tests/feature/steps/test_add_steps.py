import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../src")))

from tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_category, filter_tasks_by_completion, get_overdue_tasks
from behave import given, when, then

@given('an empty task list')
def step_given_empty_task_list(context):
    context.file_path = "test_tasks.json"
    if os.path.exists(context.file_path):
        os.remove(context.file_path)
    context.tasks = []

@when('I add a task with title "{title}"')
def step_when_add_task(context, title):
    task_id = generate_unique_id(context.tasks)
    new_task = {
        "id": task_id,
        "title": title,
        "description": "",
        "completed": False,
        "priority": "Medium",
        "category": None,
        "due_date": ""
    }
    context.tasks.append(new_task)
    save_tasks(context.tasks, context.file_path)

@then('the task list should contain a task titled "{title}"')
def step_then_task_in_list(context, title):
    loaded = load_tasks(context.file_path)
    assert any(t["title"] == title for t in loaded)

@given('a task titled "{title}" in the list')
def step_given_task_in_list(context, title):
    context.file_path = "test_tasks.json"
    context.tasks = []
    task_id = generate_unique_id(context.tasks)
    new_task = {
        "id": task_id,
        "title": title,
        "description": "",
        "completed": False,
        "priority": "Medium",
        "category": None,
        "due_date": ""
    }
    context.tasks.append(new_task)
    save_tasks(context.tasks, context.file_path)

@when('I mark the task "{title}" as completed')
def step_when_mark_completed(context, title):
    for task in context.tasks:
        if task["title"] == title:
            task["completed"] = True
    save_tasks(context.tasks, context.file_path)

@then('the task "{title}" should be marked completed')
def step_then_check_completed(context, title):
    loaded = load_tasks(context.file_path)
    match = next((t for t in loaded if t["title"] == title), None)
    assert match is not None and match["completed"] is True

@given('a task titled "{title}" in category "{category}"')
def step_given_task_with_category(context, title, category):
    context.file_path = "test_tasks.json"
    context.tasks = [{
        "id": 1,
        "title": title,
        "description": "",
        "completed": False,
        "priority": "Medium",
        "category": category,
        "due_date": ""
    }]
    save_tasks(context.tasks, context.file_path)

@when('I filter tasks by category "{category}"')
def step_when_filter_by_category(context, category):
    loaded = load_tasks(context.file_path)
    context.filtered = filter_tasks_by_category(loaded, category)

@then('I should see a completed task titled "{title}"')
def step_then_see_filtered_task(context, title):
    assert any(t["title"] == title for t in context.filtered)

@given('a task titled "{title}" marked completed')
def step_given_completed_task(context, title):
    context.file_path = "test_tasks.json"
    context.tasks = [{
        "id": 1,
        "title": title,
        "description": "",
        "completed": True,
        "priority": "Medium",
        "category": None,
        "due_date": ""
    }]
    save_tasks(context.tasks, context.file_path)

@when('I filter tasks to show only completed')
def step_when_filter_completed(context):
    loaded = load_tasks(context.file_path)
    context.filtered = filter_tasks_by_completion(loaded, True)

@given('a task titled "{title}" due on "{due_date}" and not completed')
def step_given_overdue_task(context, title, due_date):
    context.file_path = "test_tasks.json"
    context.tasks = [{
        "id": 1,
        "title": title,
        "description": "",
        "completed": False,
        "priority": "Medium",
        "category": None,
        "due_date": due_date
    }]
    save_tasks(context.tasks, context.file_path)

@when('I retrieve overdue tasks')
def step_when_get_overdue_tasks(context):
    loaded = load_tasks(context.file_path)
    context.filtered = get_overdue_tasks(loaded)

@then('I should see a task titled "{title}"')
def step_then_see_overdue(context, title):
    assert any(t["title"] == title for t in context.filtered)
