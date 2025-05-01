import subprocess
import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import load_tasks, save_tasks, filter_tasks_by_priority, filter_tasks_by_category, search_tasks, sort_tasks_by_due_date, mark_all_tasks_completed

def run_test(command, label):
    with st.spinner(f"Running {label}..."):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        st.text_area(f"{label} Output", result.stdout + "\n" + result.stderr, height=300)


def main():
    st.title("To-Do Application")
    
    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")
        
        if submit_button and task_title:
            new_task = {
                "id": len(tasks) + 1,
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # Search by keyword
    search_term = st.text_input("Search tasks")
    if search_term:
        filtered_tasks = search_tasks(filtered_tasks, search_term)

    # Sorting by due date
    sort_order = st.radio("Sort by Due Date", ["None", "Ascending", "Descending"], horizontal=True)
    if sort_order == "Ascending":
        filtered_tasks = sort_tasks_by_due_date(filtered_tasks, ascending=True)
    elif sort_order == "Descending":
        filtered_tasks = sort_tasks_by_due_date(filtered_tasks, ascending=False)

    # Mark all as completed
    if st.button("Mark All as Completed"):
        filtered_tasks = mark_all_tasks_completed(filtered_tasks)
        save_tasks(filtered_tasks)
        st.success("All visible tasks marked as completed.")
        st.rerun()

    # Display tasks
    for task in filtered_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

    #Run Tests
    st.sidebar.header("Run Tests")

    if st.sidebar.button("Basic Test"):
        run_test("pytest tests/test_basic.py", "Basic Test")

    if st.sidebar.button("Advanced Test"):
        run_test("pytest tests/test_advanced.py", "Advanced Test")

    if st.sidebar.button("Property Test"):
        run_test("pytest tests/test_property.py", "Property Test")

    if st.sidebar.button("TDD Test"):
        run_test("pytest tests/test_tdd.py", "TDD Test")

    if st.sidebar.button("BDD Test"):
        run_test("behave tests/feature", "BDD Test")

if __name__ == "__main__":
    main()