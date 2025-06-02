# app.py

import streamlit as st
from datetime import datetime  # ✅ this line adds timestamp support

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

    else:
        response = f"I'm your agent. You said: {user_input}"

    st.session_state.history.append({"role": "agent", "content": response})
# Display chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
