import streamlit as st
from src.chatbot_handler import run_chatbot_with_input
from dotenv import load_dotenv

load_dotenv()

st.title("Chicago Crime Data Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

def send_question():
    user_question = st.session_state.user_input
    if user_question.strip() == "":
        return

    try:
        answer = run_chatbot_with_input(user_question)
    except KeyError as e:
        st.error(f"Missing expected key: {e}. Please ensure all required fields are present.")
        return
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return

    st.session_state.history.append({"user": user_question, "bot": answer})
    st.session_state.user_input = ""

st.text_input("Enter your question here:", key="user_input", on_change=send_question)

# Show chat history with latest first, so recent messages appear near input
for chat in reversed(st.session_state.history):
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Bot:** {chat['bot']}")
