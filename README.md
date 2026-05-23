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
│   ├── main.py                       # Application entry point
│   └── application/                  # Main application package
│       ├── app.py                    # FastAPI app factory
│       ├── api/                      # API routes and endpoints
│       │   ├── auth.py              # Authentication endpoints
│       │   ├── posts.py             # Post management
│       │   ├── users.py             # User management
│       │   ├── categories.py        # Category management
│       │   ├── locations.py         # Location management
│       │   ├── comments.py          # Comment management
│       │   ├── admin.py             # Admin endpoints
│       │   └── depends.py           # Dependency injection
│       ├── core/                     # Core functionality
│       │   ├── config.py            # Configuration settings
│       │   ├── logging_config.py    # Logging setup
│       │   └── exceptions/          # Custom exceptions
│       ├── domain/                   # Business logic (use cases)
│       │   ├── auth/                # Authentication logic
│       │   ├── user/                # User operations
│       │   ├── post/                # Post operations
│       │   ├── category/            # Category operations
│       │   ├── location/            # Location operations
│       │   └── comment/             # Comment operations
│       ├── infrastructure/           # External services
│       │   └── database/            # Database layer
│       │       ├── database.py      # Database connection
│       │       ├── models/          # SQLAlchemy models
│       │       └── repositories/    # Data access layer
│       ├── schemas/                  # Pydantic schemas
│       ├── services/                 # Application services
│       └── resources/                # Shared resources
├── tests/                            # Test suite
│   ├── conftest.py                  # Root fixtures (fake_session, fake_db)
│   ├── mocks.py                     # FakeSession & FakeDatabase
│   ├── test_api/                    # API endpoint tests
│   │   ├── conftest.py             # async_client, auth fixtures
│   │   ├── base.py                 # Shared CRUD assertion helpers
│   │   ├── test_admin.py
│   │   ├── test_auth.py
│   │   ├── test_categories.py
│   │   ├── test_comments.py
│   │   ├── test_locations.py
│   │   ├── test_posts.py
│   │   └── test_users.py
│   ├── test_schemas/                # Pydantic schema validation tests
│   └── test_use_cases/              # Unit tests for use cases
├── alembic/                          # Database migrations
│   └── versions/
├── static/images/                    # Uploaded post images
├── postman/                          # Load testing collections
├── logs/
├── pyproject.toml                    # Project configuration
├── pytest.ini                        # Pytest configuration
├── alembic.ini                       # Alembic configuration
├── Dockerfile                        # Docker build
└── docker-compose.yml                # Docker setup
```

## Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory based on `.env_example`:

```bash
cp .env_example .env
```

Key database variables:
- `POSTGRES_HOST`: Hostname of the PostgreSQL server.
- `POSTGRES_PORT`: Port of the PostgreSQL server.
- `POSTGRES_USER`: Database user.
- `POSTGRES_PASSWORD`: Database password.
- `POSTGRES_DB`: Database name.

## Running the Application

Depending on your environment, you can run the application in several ways:

### 1. Full Docker Setup (Recommended)
Run the entire stack (backend and database) in containers:
```bash
docker compose up -d
```
The application will be available at `http://localhost:8020`.

### 2. Hybrid Setup (Local Backend $\rightarrow$ Docker DB)
This is ideal for development as it allows for faster code reloading.

1. Start only the database container:
   ```bash
   docker compose up -d postgres
   ```

2. Configure your `.env` file for local access:
   ```env
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5436
   ```

3. Run the application locally:
   ```bash
   python src/main.py
   ```
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
The server will start on `http://0.0.0.0:8000`.
