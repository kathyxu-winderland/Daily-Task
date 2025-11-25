import streamlit as st
import datetime
import json
import os

# --- Configuration ---
FILE_NAME = 'tasks.json'

# --- Functions ---
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return {"work": [], "personal": []}
    try:
        with open(FILE_NAME, 'r') as f:
            return json.load(f)
    except:
        return {"work": [], "personal": []}

def save_tasks(tasks):
    with open(FILE_NAME, 'w') as f:
        json.dump(tasks, f)

# --- App Layout ---
st.set_page_config(page_title="Daily Dashboard", page_icon="📅", layout="centered")

st.title("📅 Unified Daily Dashboard")
st.caption(f"Date: {datetime.date.today()}")

# Load data
tasks = load_tasks()

# --- INPUT SECTION ---
with st.expander("➕ Add New Task", expanded=False):
    col1, col2 = st.columns([3, 1])
    with col1:
        new_task = st.text_input("Task Name")
    with col2:
        category = st.selectbox("Category", ["Work", "Personal"])
    
    if st.button("Add Task"):
        if new_task:
            cat_key = category.lower()
            tasks[cat_key].append({"task": new_task, "done": False})
            save_tasks(tasks)
            st.rerun()

st.divider()

# --- VIEW SECTION ---
col_work, col_life = st.columns(2)

with col_work:
    st.header("💼 Work")
    # Use index to create unique keys
    for i, item in enumerate(tasks["work"]):
        check = st.checkbox(item["task"], value=item["done"], key=f"work_{i}")
        if check != item["done"]:
            tasks["work"][i]["done"] = check
            save_tasks(tasks)
            st.rerun()

with col_life:
    st.header("❤️ Personal")
    for i, item in enumerate(tasks["personal"]):
        check = st.checkbox(item["task"], value=item["done"], key=f"pers_{i}")
        if check != item["done"]:
            tasks["personal"][i]["done"] = check
            save_tasks(tasks)
            st.rerun()

# --- CLEAR BUTTON ---
if st.button("🗑️ Clear Completed Tasks"):
    tasks["work"] = [t for t in tasks["work"] if not t["done"]]
    tasks["personal"] = [t for t in tasks["personal"] if not t["done"]]
    save_tasks(tasks)
    st.rerun()