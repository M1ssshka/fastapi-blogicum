# Blogicum

A FastAPI-based blog application with clean architecture.

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
   git clone <repository-url>
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
blogicum/
├── src/
│   ├── main.py                    # Application entry point
│   └── application/               # Main application package
│       ├── api/                   # API routes and endpoints
│       │   ├── auth.py           # Authentication endpoints
│       │   ├── posts.py          # Post management
│       │   ├── users.py          # User management
│       │   ├── categories.py     # Category management
│       │   ├── locations.py      # Location management
│       │   ├── comments.py       # Comment management
│       │   └── depends.py        # Dependency injection
│       ├── core/                  # Core functionality
│       │   ├── config.py         # Configuration settings
│       │   ├── logging_config.py # Logging setup
│       │   └── exceptions/       # Custom exceptions
│       ├── domain/                # Business logic (use cases)
│       │   ├── auth/             # Authentication logic
│       │   ├── user/             # User operations
│       │   ├── post/             # Post operations
│       │   ├── category/         # Category operations
│       │   ├── location/         # Location operations
│       │   └── comment/          # Comment operations
│       ├── infrastructure/        # External services
│       │   └── database/         # Database layer
│       │       ├── database.py   # Database connection
│       │       ├── models/       # SQLAlchemy models
│       │       └── repositories/ # Data access layer
│       ├── schemas/               # Pydantic schemas
│       ├── services/              # Application services
│       └── resources/             # Shared resources
├── alembic/                       # Database migrations
├── pyproject.toml                 # Project configuration
├── alembic.ini                    # Alembic configuration
└── docker-compose.yml             # Docker setup
```

## Running the Application

### Local Development

1. Run the application:
   ```bash
   python src/main.py
   ```

   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

The server will start on `http://0.0.0.0:8000`.
