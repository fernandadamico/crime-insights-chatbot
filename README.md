# Crime Insights Chatbot

This project is a conversational interface designed to help users explore crime data from Chicago (2020–2022) in a more intuitive way. It uses a local large language model (via **Ollama**) and a lightweight **SQLite** database to turn natural language questions into insightful answers — no need to write SQL.

The chatbot aims to make the data more accessible and easier to understand.

---

## Features

- Ask natural language questions about crimes in Chicago (2020–2022)

- Automatically converts your questions into SQL queries

- Runs queries on a local SQLite database

- Generates clear, human-readable answers using a local LLM

- Simple and interactive web interface built with Streamlit


---

## More Details

For a deeper look into how this chatbot was built — including design decisions, architecture, and testing — you can check the `docs/report.md` file. It covers:

- **Architecture and Design Decisions**  
- **Component Breakdown**  
- **Design Choices and Justifications**  
- **Validation and Testing**

You’ll also find a **video demo**, showing the chatbot in action!

## Setup Instructions

### Prerequisites
Before running this project, please make sure you have the following installed and configured on your machine:

- **Python 3.10 or higher** – This project relies on features available in recent Python versions.
- **[Ollama](https://ollama.com/)** - You’ll need Ollama installed and running locally, as the chatbot uses an LLM (Large Language Model) through Ollama to generate and interpret queries. 
- **Raw CSV files from the City of Chicago Data Portal** – The SQLite database is *not included* in the repository. Instead, a script is provided to build the database automatically from official public data. No need to download or create it manually.
- **Virtual Environment (optional, but recommended)** – I suggest using a virtual environment (via venv or Conda) to manage dependencies without affecting your global Python setup.

If you're using Conda, there is also an environment.yml file to help set things up quickly.


---

### Installation

1. **Clone this repository**
```bash
git clone https://github.com/yourusername/crime-insights-chatbot.git
cd crime-insights-chatbot
```

2. **Create and activate a virtual environment**

Using venv:
```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Windows CMD
.\venv\Scripts\activate.bat
# macOS/Linux
source venv/bin/activate
```

Or using Conda:
```bash
conda env create -f environment.yml
conda activate crime-chatbot
```
3. **Install dependencies**

```bash
pip install -r requirements.txt
```
4. **Set environment variables**

Create a .env file in the project root:
```bash
TOGETHER_API_KEY=your_api_key_here
OLLAMA_MODEL=gemma3
```
5. **Download data and generate the SQLite database**
```bash
python data/data_pipeline.py
python data/create_sql.py
```

6. **Run the Streamlit app**
```bash
streamlit run src/main.py
```

---

## Usage

Using the chatbot is simple and intuitive — just follow these steps:

- Type any crime-related question (like “How many thefts happened in 2021?”) in the input box.

- You'll see the answer right away, and you can scroll through your previous questions too!

- If you're using the CLI version, just type exit anytime to close it.

---

## Notes
- Make sure the **Ollama** daemon is running locally with the model you’ve chosen. If it’s your first time, you may need to pull a model (e.g. gemma) using the ollama run command.

- The SQLite database (data/crimes.db) will be created automatically from public data the first time you run the project — no need to download or create anything manually!

- The project also uses Together AI behind the scenes to summarize answers in natural language, giving you quick, friendly responses.