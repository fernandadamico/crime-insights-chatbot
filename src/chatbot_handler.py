import pandas as pd
from src.intent_parser import parse_user_input
from src.crime_data_filter import filter_crimes, summarize_crimes_compact
from src.model_response import construct_prompt, ask_question_with_together

def run_chatbot_with_input(user_question):
    # Load dataset
    df = pd.read_csv("data/crimes_chicago.csv", low_memory=False, parse_dates=["date"])
    
    # Ensure datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['date_only'] = df['date'].dt.date

    # Extract known crime types from dataset for parsing
    known_crime_types = df['primary_type'].unique().tolist()

    # Parse user question to extract structured intent
    parsed = parse_user_input(user_question, known_crime_types)

    # Apply filters based on parsed input
    filtered_df = filter_crimes(df, parsed)

    # Count number of matching crimes
    crime_count = len(filtered_df)

    # Generate compact summary of filtered crimes
    summary_text = summarize_crimes_compact(filtered_df)

    # Construct the final prompt using the template
    prompt = construct_prompt(
        question=user_question,
        parsed_input=parsed,
        crime_count=crime_count,
        summary_text=summary_text
    )

    # Get response from LLM
    answer = ask_question_with_together(prompt)

    return answer
