"""
Utils module for SmartTodo application.
Contains business logic, data operations, filtering, sorting, and reporting.
"""

import json
import os
import uuid
from datetime import datetime, date, time
from typing import List, Dict, Any, Optional
import pandas as pd

DB_FILE = "database.json"

def initialize_database() -> None:
    """
    Ensure the JSON database file exists and is valid.
    If database.json is missing, empty, or corrupt, initialize it with {"tasks": []}.
    """
    default_structure = {"tasks": []}
    
    if not os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_structure, f, indent=4)
        except Exception as e:
            print(f"Error initializing database file: {e}")
            return
            
    # If file exists, verify it's valid JSON with 'tasks' key
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                # File is empty
                raise ValueError("Empty file")
            data = json.loads(content)
            if not isinstance(data, dict) or "tasks" not in data:
                raise ValueError("Invalid structure")
    except (json.JSONDecodeError, ValueError, IOError) as e:
        # Re-initialize the file with empty tasks
        try:
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_structure, f, indent=4)
        except Exception as write_err:
            print(f"Error resetting database file: {write_err}")


def load_tasks() -> List[Dict[str, Any]]:
    """
    Load the list of tasks from the database file.
    Always returns a list, even if reading fails.
    """
    initialize_database()
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("tasks", [])
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []


def save_tasks(tasks: List[Dict[str, Any]]) -> bool:
    """
    Save the list of tasks to the database file.
    Returns True if successful, False otherwise.
    """
    try:
        # Safeguard structure
        data = {"tasks": tasks}
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving tasks: {e}")
        return False


def add_task(
    title: str,
    description: str,
    category: str,
    priority: str,
    due_date: str,
    due_time: str,
    status: str = "Pending"
) -> Optional[Dict[str, Any]]:
    """
    Create a new task, assign automatic UUID and creation times, and save to database.
    Returns the created task dictionary or None if saving failed.
    """
    now = datetime.now()
    created_date = now.strftime("%Y-%m-%d")
    created_time = now.strftime("%H:%M:%S")
    last_updated = now.strftime("%Y-%m-%d %H:%M:%S")
    
    new_task = {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "description": description.strip() if description else "",
        "category": category,
        "priority": priority,
        "status": status,
        "created_date": created_date,
        "created_time": created_time,
        "due_date": due_date,
        "due_time": due_time,
        "last_updated": last_updated
    }
    
    tasks = load_tasks()
    tasks.append(new_task)
    
    if save_tasks(tasks):
        return new_task
    return None


def update_task(
    task_id: str,
    title: str,
    description: str,
    category: str,
    priority: str,
    due_date: str,
    due_time: str,
    status: str
) -> bool:
    """
    Update details of an existing task matching task_id and refresh last_updated.
    Returns True if updated successfully, False otherwise.
    """
    tasks = load_tasks()
    found = False
    
    for task in tasks:
        if task.get("id") == task_id:
            task["title"] = title.strip()
            task["description"] = description.strip() if description else ""
            task["category"] = category
            task["priority"] = priority
            task["due_date"] = due_date
            task["due_time"] = due_time
            task["status"] = status
            task["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break
            
    if found:
        return save_tasks(tasks)
    return False


def delete_task(task_id: str) -> bool:
    """
    Permanently delete a task from the database.
    Returns True if found and deleted, False otherwise.
    """
    tasks = load_tasks()
    initial_length = len(tasks)
    tasks = [task for task in tasks if task.get("id") != task_id]
    
    if len(tasks) < initial_length:
        return save_tasks(tasks)
    return False


def complete_task(task_id: str) -> bool:
    """
    Transition task status from Pending to Completed.
    Updates last_updated and saves.
    """
    tasks = load_tasks()
    found = False
    
    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = "Completed"
            task["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break
            
    if found:
        return save_tasks(tasks)
    return False


def search_tasks(tasks: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Search tasks list matching query in title, description, or category.
    Case-insensitive search.
    """
    if not query:
        return tasks
        
    query = query.lower().strip()
    results = []
    for task in tasks:
        title = task.get("title", "").lower()
        desc = task.get("description", "").lower()
        cat = task.get("category", "").lower()
        
        if query in title or query in desc or query in cat:
            results.append(task)
    return results


def filter_tasks(tasks: List[Dict[str, Any]], filter_name: str) -> List[Dict[str, Any]]:
    """
    Filter tasks list based on predetermined criteria (e.g. status, priority, due date).
    """
    if filter_name == "All":
        return tasks
        
    if filter_name in ["Pending", "Completed"]:
        return [task for task in tasks if task.get("status") == filter_name]
        
    if filter_name in ["High Priority", "Medium Priority", "Low Priority"]:
        priority_level = filter_name.split()[0] # "High", "Medium", "Low"
        return [task for task in tasks if task.get("priority") == priority_level]
        
    if filter_name in ["Personal", "Study", "Work", "Shopping", "Others"]:
        return [task for task in tasks if task.get("category") == filter_name]
        
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if filter_name == "Today's Tasks":
        return [task for task in tasks if task.get("due_date") == today_str]
        
    if filter_name == "Overdue Tasks":
        overdue_tasks = []
        now_dt = datetime.now()
        for task in tasks:
            if task.get("status") == "Completed":
                continue
            due_date_str = task.get("due_date")
            due_time_str = task.get("due_time", "23:59")
            
            if not due_date_str:
                continue
                
            try:
                # Parse due date & time
                if due_time_str:
                    due_dt = datetime.strptime(f"{due_date_str} {due_time_str}", "%Y-%m-%d %H:%M")
                else:
                    due_dt = datetime.strptime(due_date_str, "%Y-%m-%d").replace(hour=23, minute=59)
                
                if due_dt < now_dt:
                    overdue_tasks.append(task)
            except ValueError:
                # If timestamp fails to parse, fallback to date comparison
                if due_date_str < today_str:
                    overdue_tasks.append(task)
        return overdue_tasks
        
    return tasks


def sort_tasks(tasks: List[Dict[str, Any]], sort_by: str) -> List[Dict[str, Any]]:
    """
    Sort tasks list based on:
    - Newest First
    - Oldest First
    - Priority (High -> Medium -> Low)
    - Due Date (Earliest to Latest)
    - Alphabetically (A-Z)
    """
    if not tasks:
        return tasks
        
    def get_creation_dt(t: Dict[str, Any]) -> datetime:
        try:
            return datetime.strptime(f"{t.get('created_date')} {t.get('created_time')}", "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError):
            return datetime.min

    def get_due_dt(t: Dict[str, Any]) -> datetime:
        due_date_str = t.get("due_date")
        due_time_str = t.get("due_time")
        if not due_date_str:
            return datetime.max # Put items without due dates at the end
        try:
            if due_time_str:
                return datetime.strptime(f"{due_date_str} {due_time_str}", "%Y-%m-%d %H:%M")
            return datetime.strptime(due_date_str, "%Y-%m-%d").replace(hour=23, minute=59)
        except (ValueError, TypeError):
            return datetime.max

    if sort_by == "Newest First":
        return sorted(tasks, key=get_creation_dt, reverse=True)
        
    elif sort_by == "Oldest First":
        return sorted(tasks, key=get_creation_dt)
        
    elif sort_by == "Priority":
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        return sorted(tasks, key=lambda x: priority_map.get(x.get("priority", "Low"), 3))
        
    elif sort_by == "Due Date":
        return sorted(tasks, key=get_due_dt)
        
    elif sort_by == "Alphabetically":
        return sorted(tasks, key=lambda x: x.get("title", "").lower())
        
    return tasks


def export_csv(tasks: List[Dict[str, Any]]) -> str:
    """
    Convert tasks list to CSV string.
    """
    if not tasks:
        return ""
    df = pd.DataFrame(tasks)
    return df.to_csv(index=False)


def export_json(tasks: List[Dict[str, Any]]) -> str:
    """
    Convert tasks list to formatted JSON string.
    """
    return json.dumps({"tasks": tasks}, indent=4)


def import_json(json_content: str) -> bool:
    """
    Validate and merge or replace the database tasks list with uploaded JSON content.
    Returns True if successfully imported, False otherwise.
    """
    try:
        data = json.loads(json_content)
        if not isinstance(data, dict) or "tasks" not in data:
            return False
            
        imported_tasks = data["tasks"]
        if not isinstance(imported_tasks, list):
            return False
            
        # Basic schema verification for imported tasks
        validated_tasks = []
        for task in imported_tasks:
            if not isinstance(task, dict) or "title" not in task:
                continue # Skip invalid items
                
            # Populate defaults for missing keys to ensure backwards compatibility
            clean_task = {
                "id": task.get("id", str(uuid.uuid4())),
                "title": task.get("title", "Untitled").strip(),
                "description": task.get("description", "").strip(),
                "category": task.get("category", "Others"),
                "priority": task.get("priority", "Medium"),
                "status": task.get("status", "Pending"),
                "created_date": task.get("created_date", datetime.now().strftime("%Y-%m-%d")),
                "created_time": task.get("created_time", datetime.now().strftime("%H:%M:%S")),
                "due_date": task.get("due_date", ""),
                "due_time": task.get("due_time", ""),
                "last_updated": task.get("last_updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            }
            validated_tasks.append(clean_task)
            
        # Overwrite current database
        return save_tasks(validated_tasks)
    except Exception as e:
        print(f"Error importing JSON: {e}")
        return False


def calculate_statistics(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary statistics of the tasks.
    """
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("status") == "Completed")
    pending = total - completed
    
    # Overdue count
    overdue_list = filter_tasks(tasks, "Overdue Tasks")
    overdue = len(overdue_list)
    
    # Today's tasks
    today_list = filter_tasks(tasks, "Today's Tasks")
    today = len(today_list)
    
    # Priority counts
    high = sum(1 for t in tasks if t.get("priority") == "High")
    medium = sum(1 for t in tasks if t.get("priority") == "Medium")
    low = sum(1 for t in tasks if t.get("priority") == "Low")
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue,
        "today": today,
        "high": high,
        "medium": medium,
        "low": low
    }


def load_custom_css() -> None:
    """
    Inject assets/style.css stylesheet into Streamlit.
    """
    import streamlit as st
    css_path = os.path.join("assets", "style.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r", encoding="utf-8") as f:
                css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading CSS: {e}")


def render_sidebar(tasks: List[Dict[str, Any]]) -> None:
    """
    Render a cohesive sidebar across all pages.
    """
    import streamlit as st
    from datetime import datetime
    
    # Header logo and branding
    st.sidebar.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
            <span style="font-size: 2.2rem; filter: drop-shadow(0 0 4px rgba(139, 92, 246, 0.4));">🎯</span>
            <div>
                <h2 style="margin: 0; font-size: 1.4rem; font-weight: 800; background: linear-gradient(135deg, #a78bfa, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">SmartTodo</h2>
                <p style="margin: 0; font-size: 0.75rem; opacity: 0.6; font-weight: 500;">Version 1.0</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    
    # Current Date and Time Widget
    now = datetime.now()
    date_str = now.strftime("%A, %b %d, %Y")
    time_str = now.strftime("%I:%M %p")
    
    st.sidebar.markdown(
        f"""
        <div class="sidebar-time-container">
            <div style="font-weight: 600; font-size: 0.85rem; opacity: 0.8;">{date_str}</div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #a78bfa; margin-top: 4px; letter-spacing: 0.5px;">{time_str}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown("---")
    
    # Quick Statistics Indicator
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.get("status") == "Completed")
    pending_tasks = total_tasks - completed_tasks
    
    st.sidebar.markdown("### Quick Progress")
    
    # Completion Bar
    if total_tasks > 0:
        progress_pct = int((completed_tasks / total_tasks) * 100)
        st.sidebar.markdown(f"**Completion Rate:** `{progress_pct}%` ({completed_tasks}/{total_tasks})")
        st.sidebar.progress(completed_tasks / total_tasks)
    else:
        st.sidebar.markdown("*No tasks recorded yet.*")
        st.sidebar.progress(0.0)
        
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="font-size: 0.75rem; opacity: 0.5; text-align: center; margin-top: 30px;">
            Made with ❤️ using Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

