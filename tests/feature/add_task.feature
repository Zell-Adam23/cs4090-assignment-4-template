Feature: Manage To-Do Tasks

    Scenario: Add a task to the task list
        Given an empty task list
        When I add a task with title "Buy groceries"
        Then the task list should contain a task titled "Buy groceries"

    Scenario: Mark a task as completed
        Given a task titled "Finish homework" in the list
        When I mark the task "Finish homework" as completed
        Then the task "Finish homework" should be marked completed

    Scenario: Filter tasks by category
        Given a task titled "Submit project" in category "Work"
        When I filter tasks by category "Work"
        Then I should see a task titled "Submit project"

    Scenario: Filter tasks by completion
        Given a task titled "Meditate" marked completed
        When I filter tasks to show only completed
        Then I should see a task titled "Meditate"

    Scenario: Get overdue tasks
        Given a task titled "Submit tax forms" due on "2024-01-01" and not completed
        When I retrieve overdue tasks
        Then I should see a task titled "Submit tax forms"