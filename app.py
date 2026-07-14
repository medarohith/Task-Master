"""
SmartTodo - Main Application File
Implements the main dashboard of the multi-page application.
"""

import os
from datetime import datetime, date, time
import streamlit as st
from dotenv import load_dotenv
import utils

# Load environment variables
load_dotenv()
APP_NAME = os.getenv("APP_NAME", "SmartTodo")
VERSION = os.getenv("VERSION", "1.0")

# Set up page configurations
st.set_page_config(
    page_title=f"{APP_NAME} - Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global CSS
utils.load_custom_css()

# Retrieve latest tasks data
tasks = utils.load_tasks()

# Render shared sidebar
utils.render_sidebar(tasks)

# Main Page Header
st.markdown(
    f"""
    <div style="background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(236,72,153,0.1)); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 25px;">
        <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; color: inherit;">🎯 Welcome to {APP_NAME} Dashboard</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.8; font-size: 1.05rem;">Your ultimate productivity companion. Let's organize and conquer your tasks today!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Statistics & Analytics
stats = utils.calculate_statistics(tasks)

# Metric cards using HTML columns inside streamlit columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 4px solid #8b5cf6;">
            <div class="metric-value" style="color: #8b5cf6;">{stats['total']}</div>
            <div class="metric-label">Total Tasks</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 4px solid #10b981;">
            <div class="metric-value" style="color: #10b981;">{stats['completed']}</div>
            <div class="metric-label">Completed</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 4px solid #ef4444;">
            <div class="metric-value" style="color: #ef4444;">{stats['pending']}</div>
            <div class="metric-label">Pending</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 4px solid #f59e0b;">
            <div class="metric-value" style="color: #f59e0b;">{stats['overdue']}</div>
            <div class="metric-label">Overdue</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Section split into two columns: Left (Upcoming/Calendar agenda), Right (Recent activity summaries)
left_col, right_col = st.columns([3, 2])

with left_col:
    st.subheader("📅 Calendar / Agenda View")
    
    # Sort tasks by due date (earliest first)
    pending_tasks = [t for t in tasks if t.get("status") == "Pending"]
    sorted_by_due = utils.sort_tasks(pending_tasks, "Due Date")
    
    if sorted_by_due:
        # Show agenda list
        st.write("Below is a breakdown of your upcoming pending tasks, ordered by due date:")
        for t in sorted_by_due[:5]: # Show top 5 upcoming
            due_date_str = t.get("due_date", "No Due Date")
            due_time_str = t.get("due_time", "")
            
            # Format time display
            due_display = f"{due_date_str}" + (f" at {due_time_str}" if due_time_str else "")
            priority_val = t.get("priority", "Medium")
            cat_val = t.get("category", "Others")
            
            badge_priority_class = f"badge-priority-{priority_val.lower()}"
            badge_cat_class = f"badge-category-{cat_val.lower()}"
            
            st.markdown(
                f"""
                <div class="task-card" style="padding: 15px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <span class="task-title" style="font-size: 1.1rem;">{t.get('title')}</span>
                        <div class="badge-container" style="margin-bottom: 0;">
                            <span class="badge {badge_priority_class}">{priority_val}</span>
                            <span class="badge {badge_cat_class}">{cat_val}</span>
                        </div>
                    </div>
                    <p style="font-size: 0.85rem; opacity: 0.8; margin: 5px 0 10px 0;">{t.get('description', '')[:100]}...</p>
                    <div style="font-size: 0.8rem; opacity: 0.6; display: flex; align-items: center; gap: 5px;">
                        <span>📅 Due: <strong>{due_display}</strong></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if len(sorted_by_due) > 5:
            st.info(f"And {len(sorted_by_due) - 5} more pending task(s). Visit the History page to view all.")
    else:
        st.info("No upcoming pending tasks. Great job!")

with right_col:
    # Bonus Feature: Recently Added
    st.subheader("⚡ Recently Added")
    newest_tasks = utils.sort_tasks(tasks, "Newest First")
    
    if newest_tasks:
        for t in newest_tasks[:3]:
            title = t.get("title")
            cat = t.get("category")
            status = t.get("status")
            status_class = f"badge-status-{status.lower()}"
            
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <div>
                        <span style="font-weight: 600; font-size: 0.95rem;">{title}</span>
                        <br/>
                        <span style="font-size: 0.75rem; opacity: 0.6;">Added: {t.get('created_date')}</span>
                    </div>
                    <div style="display: flex; gap: 5px;">
                        <span class="badge {status_class}" style="font-size: 0.65rem; padding: 2px 6px;">{status}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No tasks found.")
        
    st.write("")
    
    # Bonus Feature: Recently Completed
    st.subheader("🏆 Recently Completed")
    completed_list = [t for t in tasks if t.get("status") == "Completed"]
    # Sort completed by last updated to get the most recently completed
    completed_sorted = sorted(completed_list, key=lambda x: x.get("last_updated", ""), reverse=True)
    
    if completed_sorted:
        for t in completed_sorted[:3]:
            title = t.get("title")
            cat = t.get("category")
            
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <div>
                        <span style="font-weight: 600; font-size: 0.95rem; text-decoration: line-through; opacity: 0.7;">{title}</span>
                        <br/>
                        <span style="font-size: 0.75rem; opacity: 0.6;">Completed: {t.get('last_updated')[:10]}</span>
                    </div>
                    <span class="badge badge-category-{cat.lower()}" style="font-size: 0.65rem; padding: 2px 6px;">{cat}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No tasks completed yet. You can do it!")

st.markdown("---")

# Quick tips for user
st.markdown("### 💡 Quick Guide")
st.markdown(
    """
    * Navigate to the **Task Manager** page from the sidebar to create new tasks.
    * Use the **History** page to filter, search, view, edit, or delete your tasks, and check visual statistics charts.
    * Adjust configurations, reset your database, or export/import data in the **Settings** page.
    """
)
