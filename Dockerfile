ARG PYTHON_VERSION=3.14

# ------------------------ BASE ------------------------
FROM python:${PYTHON_VERSION}-slim AS base

ENV APPDIR=/app

ENV TZ=America/Mexico_City \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/venv" \
    PATH="/venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --chmod=755 ./bin /usr/local/bin

WORKDIR $APPDIR

COPY pyproject.toml uv.lock* ./

# ------------------------ LOCAL ------------------------
FROM base AS local

ENV ENVIRONMENT=local

RUN apt-get update \
    && apt-get install -y --no-install-recommends wget procps \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync


# ------------------------ PRODUCTION ------------------------
FROM base AS production

ENV ENVIRONMENT=production \
    UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev
