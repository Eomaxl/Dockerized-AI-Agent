# Dockerized-AI-Agent
## Project Purpose
This folder contains the core of your AI email‐generating "agent":
- Receives user messages via FastAPI (routing.py)
- Stores them in PostgreSQL via SQLModel (models.py, db.py)
- Sends user messages to OpenAI (via LangChain + ChatOpenAI)
- Returns a generated email reply
- Includes Docker support for easy deployment

## Requirements
- Python 3.10+
- PostgreSQL (connection via DATABASE_URL)
- OpenAI credentials (OPENAI_API_KEY, optionally OPENAI_BASE_URL)
- Docker & Docker Compose

## How It Works — Code Flow
- FastAPI endpoint at /api/chats/ accepts a JSON payload with message.
- SQLModel validates the payload and creates a ChatMessage record with timestamp.
- Before generating the email, it commits the record to DB.
- LangChain + ChatOpenAI sends the user message to the LLM.
- The generated response is returned in the HTTP response.

## Dockerization
- The root Dockerfile installs dependencies and starts FastAPI with Uvicorn.
- docker-compose.yml brings up both the API and a Postgres container.
- Environment variables are provided via a .env (added to .gitignore) to protect secrets.

## Performance Handling
- DB caching: Completed messages are stored with timestamps.
- Concurrency: FastAPI + Uvicorn handles multiple simultaneous requests.
- LLM generation is performed asynchronously through LangChain, non-blocking.