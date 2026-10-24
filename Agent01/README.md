# Agent01 — A Simple Personal AI Agent

Agent01 is a small personal AI assistant I built for practice while learning AI agent development.

I created this project as a hands-on experiment to understand how an AI agent works, how to connect it to a language model, and how to give it simple tools to use.

## Features

- **AI conversations:** Chat with an LLM through the GapGPT API.
- **Current date and time:** Get the current local date and time.
- **Basic calculator:** Perform arithmetic operations such as addition, subtraction, multiplication, and division.
- **Save notes:** Save simple text notes to a local file.
- **Read notes:** Retrieve previously saved notes.
- **Conversation history:** Keep the conversation context during the current session.
- **Error debugging:** Print detailed error tracebacks to the terminal to help identify and troubleshoot runtime issues.

## Tech Stack

- Python
- Pydantic AI
- GapGPT API
- OpenAI-compatible API
- python-dotenv

## Project Structure

```text
Agent01/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

The `.env` file and `notes.txt` are created or used locally and are not included in this example structure.

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Agent01
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file based on `.env.example` and add your own GapGPT API key.

```dotenv
GAPGPT_API_KEY=your_api_key_here
GAPGPT_BASE_URL=https://api.gapgpt.app/v1
GAPGPT_MODEL=gapgpt-qwen-3.5
```

**Important:** Never commit or share your real API key.

### 4. Run the agent

```bash
python main.py
```

Type your message in the terminal to start chatting. Type `quit` or `exit` to stop the program.

## Notes

Saved notes are stored locally in `notes.txt`. Conversation history is maintained while the program is running and is not saved as persistent chat history.

## Disclaimer

This is a beginner-friendly learning project built for practice and experimentation. It is not intended to be a production-ready application.

Thanks for checking out my project!