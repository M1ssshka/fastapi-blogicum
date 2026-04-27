FROM python:3.13.13-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apk add --no-cache gcc musl-dev postgresql-dev

ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=/app/src
ENV UV_SYSTEM_PYTHON=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY ./src ./src

RUN chmod +x ./src/start.sh

RUN uv sync --frozen --no-dev

COPY alembic ./alembic
COPY alembic.ini ./

EXPOSE 8000
