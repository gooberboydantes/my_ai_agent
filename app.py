# app.py

import streamlit as st
from datetime import datetime  # ✅ this line adds timestamp support

from datetime import datetime

def save_task(task_text):
    with open("tasks.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M] ")
        f.write(f"{timestamp}{task_text}\n")

def get_tasks():
    try:
        with open("tasks.txt", "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def remove_task(index):
    tasks = get_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        with open("tasks.txt", "w", encoding="utf-8") as f:
            f.writelines(tasks)
        return True
    return False


st.set_page_config(page_title="Agent V.1", layout="centered")
st.title("Agent Under Progress")

def save_note(note_text):
    with open("notes.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        f.write(f"[{timestamp}] {note_text}\n")

# Session memory
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input
user_input = st.chat_input("Type your command here...")

# Handle input
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    if user_input.lower().startswith("note:"):
            note_text = user_input[5:].strip()
            save_note(note_text)
            response = "✅ Note saved."

    elif "show notes" in user_input.lower():
            try:
                with open("notes.txt", "r", encoding="utf-8") as f:
                    notes = f.read().strip()
                response = f"📓 Here are your notes:\n\n{notes if notes else 'No notes found.'}"
            except FileNotFoundError:
                response = "You don't have any notes yet."

    elif "clear notes" in user_input.lower():
            open("notes.txt", "w").close()
            response = "🗑 Notes cleared."
    elif user_input.lower().startswith("task:"):
        task = user_input[5:].strip()
        if task:
            save_task(task)
            response = f"📝 Task saved: {task}"
        else:
            response = "Please provide a task after 'Task:'."

    elif user_input.lower() == "show tasks":
        tasks = get_tasks()
        if tasks:
            formatted = "\n".join([f"{i+1}. {task.strip()}" for i, task in enumerate(tasks)])
            response = f"🗂 Here are your tasks:\n\n{formatted}"
        else:
            response = "No tasks found."

    elif user_input.lower().startswith("complete task"):
        try:
            index = int(user_input.lower().split("complete task")[1].strip()) - 1
            if remove_task(index):
                response = f"✅ Task {index+1} completed and removed."
            else:
                response = "Invalid task number."
        except (IndexError, ValueError):
            response = "Please specify a valid task number like 'Complete task 2'."

    else:
        response = f"I'm your agent. You said: {user_input}"

        


    st.session_state.history.append({"role": "agent", "content": response})
# Display chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
