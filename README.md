# Reliable Pure Python AI Assistant

A beginner-friendly Python project exploring how to build more reliable AI assistants using simple, practical building blocks.

The project demonstrates how an AI application can interact with an LLM, use tools, validate inputs, manage conversation state, route requests, chain prompts, and run independent AI tasks in parallel.

## Project Goals

- Understand how AI assistants work through practical Python examples.
- Learn to control tool execution and handle errors.
- Explore different ways to organize AI tasks.
- Practice writing automated tests for AI application logic.
- Build a project that demonstrates my learning in AI engineering.

## Concepts Demonstrated

| Concept | Example file | What it demonstrates |
|---|---|---|
| Basic AI assistant and tool calling | `main.py` | A starting point for interacting with an AI model and tools |
| Reliable tool execution | `reliable_tool_loop.py` | Bounded tool execution and protection against excessive tool calls |
| Document tool | `document_tool_demo.py` | Reading an approved document and handling missing or empty documents |
| Conversation state | `conversation_session.py`, `conversation_memory.py` | Managing conversation interaction IDs and continuing conversations |
| Prompt chaining | `prompt_chaining.py` | Using the output of one AI task as input to a subsequent task |
| Request routing | `routing_demo.py` | Classifying requests and directing them to appropriate handlers |
| Basic parallelization | `parallelization_demo.py` | Comparing sequential and parallel execution using simulated tasks |
| Parallel AI tasks | `parallel_ai_tasks.py` | Generating an explanation and study questions concurrently |

## Technologies Used

- Python
- Google Gemini API
- Google Gen AI Python SDK
- `python-dotenv`
- `unittest`
- Ruff
- `ThreadPoolExecutor` for parallel execution

## Project Structure

```text
reliable-pure-python-ai-assistant/
├── data/
│   ├── ai_agent_notes.txt
│   └── project_brief.txt
├── tests/
│   ├── test_conversation_session.py
│   ├── test_document_tool.py
│   ├── test_parallel_ai_tasks.py
│   ├── test_prompt_chaining.py
│   ├── test_reliable_tool_loop.py
│   └── test_routing_demo.py
├── .env.example
├── .gitignore
├── conversation_memory.py
├── conversation_session.py
├── document_tool_demo.py
├── main.py
├── parallel_ai_tasks.py
├── parallelization_demo.py
├── prompt_chaining.py
├── reliable_tool_loop.py
├── requirements.txt
└── routing_demo.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Harshit-Swain-25/reliable-pure-python-ai-assistant.git
cd reliable-pure-python-ai-assistant
```

### 2. Create and activate a virtual environment

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API key

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your own Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

Keep your real API key private. Never commit your `.env` file or share your API key publicly.

### 5. Run an example

For example, to explore parallel AI tasks:

```bash
python parallel_ai_tasks.py
```

You can also explore the other Python demonstration files in the project. Some examples require a working Gemini API key and may consume API quota.

## Running the Tests

Run the complete automated test suite:

```bash
python -m unittest discover -s tests -v
```

Run Ruff to check code quality:

```bash
ruff check .
```

The project has passed **28 automated tests**, and Ruff reported that all checks passed during the latest verification.

## What I Learned

Through this project, I practised:

- Separating application logic into understandable Python modules.
- Validating inputs and handling common errors.
- Controlling tool execution instead of blindly trusting model-generated requests.
- Managing conversation state and connecting multiple AI tasks.
- Choosing between sequential execution and parallel execution.
- Writing automated tests using mocks to test AI-related code without making real API requests.

## Future Improvements

Potential improvements as my understanding develops:

- Improve error recovery when one of several parallel AI tasks fails.
- Improve the documentation and usage examples.
- Add further tests as new features are implemented.

## Author

**Harshit Swain**

GitHub: [Harshit-Swain-25](https://github.com/Harshit-Swain-25)

Repository: [Reliable Pure Python AI Assistant](https://github.com/Harshit-Swain-25/reliable-pure-python-ai-assistant)
