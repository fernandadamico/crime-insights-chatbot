import streamlit as st
from chatbot import generate_sql_query, fix_domestic_in_query, execute_sql_query, summarize_answer

st.title("Crime Insights Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def submit():
    user_input = st.session_state.user_input
    if user_input:
        with st.spinner("Processing..."):
            sql_query = generate_sql_query(user_input)
            sql_query = fix_domestic_in_query(sql_query)
            # print("Generated SQL query:", sql_query) # Presents the generated query
            result = execute_sql_query(sql_query)
            answer = summarize_answer(user_input, result)

        st.session_state.history.append((user_input, answer))
        st.session_state.user_input = ""

st.text_input("Ask a question about crimes in Chicago:", key="user_input", on_change=submit)

for user_msg, bot_msg in reversed(st.session_state.history):
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Bot:** {bot_msg}")
    st.markdown("---")