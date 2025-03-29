# LLM + RAG-Based Function Execution API

## Overview
This project implements a Python-based API service that leverages Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) to dynamically retrieve and execute automation functions based on user prompts. It integrates FAISS for vector search and Google Gemini Pro for query processing.

## Features
- **LLM + RAG for Function Retrieval**: Uses an embedding model and FAISS to retrieve relevant functions based on natural language queries.
- **Function Execution**: Generates executable Python scripts dynamically using the Gemini Pro API.
- **Session Context Management**: Maintains session history in Redis Cloud to enhance function retrieval.
- **Automation Functions**: Supports a range of system automation tasks, including launching applications, retrieving system metrics, managing processes, and executing shell commands.
- **Secure Execution**: Implements safe command execution using `shlex` and subprocess handling.

## Setup
### 1. Clone the Repository
```bash
 git clone <repo-url>
 cd llm-rag-automation-api
```

### 2. Set Up Environment
#### Using Conda
```bash
conda create --name assignment python=3.10
conda activate assignment
pip install -r requirements.txt
```

#### Using Virtualenv
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Environment variables are required in multiple locations:
- **Root Directory (`.env`)**: Used for main application settings.
- **Config Directory (`src/config/.env`)**: Holds configuration-specific variables, gemini api key should be in this file.
- **Core Directory (`src/core/.env`)**: Used for Redis access.

The `.env` file in the **Core** and **Root** directories should contain the same values as they are used for Redis access.

#### Example `.env` file:
```
GEMINI_API_KEY=<your-google-gemini-api-key>
REDIS_HOST=<your-redis-host>
REDIS_PORT=<your-redis-port>
REDIS_PASSWORD=<your-redis-password>
```

### 4. Start the API
```bash
uvicorn src.api.main:app --reload
```

## Usage
### API Endpoint: `/execute`
Send a POST request to retrieve and execute a function dynamically.
Currently session_id is optional request without session_id can be made.
#### Request Body:
```json
{
  "prompt": "Open calculator",
  "session_id": "default"
}
```

#### Response:
```json
{
  "function": "open_calculator",
  "code": "import os\nos.system('calc')"
}
```

## Supported Functions
The API supports the following automation functions:
- **Application Control**: `open_chrome`, `open_calculator`, `open_notepad`
- **System Monitoring**: `get_cpu_usage`, `get_ram_usage`
- **Process Management**: `list_running_processes`, `kill_process`
- **File Operations**: `create_text_file`, `delete_file`, `list_files_in_directory`
- **Network Utilities**: `get_ip_address`, `ping_host`
- **System Actions**: `restart_system`, `shutdown_system`
- **Command Execution**: `run_shell_command`

## Context Management
- The API maintains session history using Redis Cloud.
- Each request includes a `session_id`, which ensures context-aware retrieval of functions.
- Older interactions are stored and leveraged for better function matching.
