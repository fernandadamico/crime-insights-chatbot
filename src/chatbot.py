import os
import sqlite3
from dotenv import load_dotenv
from together import Together
from langchain_ollama.llms import OllamaLLM

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

client = Together()
llm = OllamaLLM(model="gemma3")

# Prompt template for SQL generation
base_prompt = """
You are a helpful assistant that generates SQLite-compatible SQL queries to answer questions about crime data in Chicago between 2020 and 2022. You are querying a table called 'crimes' with the following columns:

- date (ISO timestamp)
- year (integer, e.g. 2021)
- primary_type (e.g., 'THEFT', 'ROBBERY', 'BATTERY', etc.)
- description
- location_description
- community_area (integer)
- arrest (boolean)
- domestic (boolean)

Always use correct `primary_type` values, and be especially careful not to confuse:
- 'THEFT' (ex: shoplifting) vs 'ROBBERY' (ex: armed robbery)
- 'ASSAULT' vs 'BATTERY'

Your job is to translate valid questions into SQL queries.
Only answer questions that can be answered directly using the available columns.

If a user asks something unrelated (e.g., "What color is the sky?" or "What is a bottle?") or something that cannot be answered with the data (e.g., "What is the average police response time?"), you must respond with:

`-- The question is out of scope. Cannot generate a valid SQL query.`

When comparing crimes, return counts for each category, not just the difference. For example:
**If the user asks “Were there more thefts or robberies in 2021?”, return both counts so the user can compare.**

Use `GROUP BY` or `COUNT(*)` as needed.
Use `STRFTIME('%Y', date)` if necessary to extract year from date, but prefer using the `year` column when available.

Only use column names that exist. Do not make assumptions.

Only return SQL. Do not return explanation or commentary.
"""

def generate_sql_query(user_question: str) -> str:
    full_prompt = base_prompt + user_question
    response = llm.invoke(full_prompt)
    clean_lines = [line for line in response.splitlines() if "```" not in line and line.strip()]
    return "\n".join(clean_lines).strip()

def fix_domestic_in_query(query: str) -> str:
    query = query.replace("domestic = 'Domestic'", "domestic = 1")
    query = query.replace("domestic = 'True'", "domestic = 1")
    query = query.replace("domestic = 'False'", "domestic = 0")
    return query

def execute_sql_query(query: str):
    conn = sqlite3.connect("data/crimes.db")
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchone()
    except Exception as e:
        return f"SQL execution error: {e}"
    finally:
        conn.close()

def summarize_answer(user_question, query_result):
    prompt = f"""
You are a helpful assistant that answers questions about Chicago crime data.

Based on the user's question and the SQL result, provide a short, direct sentence answering the question.

Do NOT explain or show your reasoning.

If the question is unrelated to crime data, answer only: "I don't know."

Keep the answer under 20 words.

Question: {user_question}
SQL Result: {query_result}

Answer:"""

    response = client.chat.completions.create(
        model="google/gemma-3n-E4B-it",
        max_tokens=50,
        temperature=0, # Low temperature to avoid hallucinations
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()

def ask_chatbot(user_question: str) -> str:
    sql_query = generate_sql_query(user_question)
    sql_query = fix_domestic_in_query(sql_query)
    result = execute_sql_query(sql_query)
    return summarize_answer(user_question, result)

if __name__ == "__main__":
    while True:
        user_question = input("\nEnter your crime data question (or 'exit' to quit): ")
        if user_question.lower() == "exit":
            break
        print("Answer:", ask_chatbot(user_question))
