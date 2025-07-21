from src.chatbot_handler import run_chatbot
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

def main():
    run_chatbot()

if __name__ == "__main__":
    main()