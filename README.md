# Blogicum

A FastAPI-based blog application.

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (Python package manager)

## Installation

1. Install `uv`:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository and navigate to the project directory:
   ```bash
   cd blogicum
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

4. Install the package in editable mode:
   ```bash
   uv pip install -e .
   ```

## Project Structure

```
fastapi-blogicum/
├── fastapi_app/       # Application wrapper
│   ├── src/           # Source code
│   └── main.py        # Entry point
├── alembic/           # Database migrations
├── pyproject.toml     # Project configuration
└── alembic.ini        # Alembic configuration
```

## Running the Server

```bash
python fastapi_app/main.py
```

The server will start on `http://0.0.0.0:8000`.

### Development Mode (with auto-reload)

```bash
uvicorn fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```
