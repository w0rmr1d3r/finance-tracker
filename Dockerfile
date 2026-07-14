# Stage 1: Build frontend (Vite -> dist/)
FROM node:20-alpine AS frontend-build

WORKDIR /app
RUN apk add --no-cache make

COPY frontend/package-lock.json frontend/package.json frontend/Makefile ./
RUN make install

COPY frontend/ ./
RUN make build


# Stage 2: Build backend dependencies
FROM python:3.14-slim AS backend-build

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apt-get update && apt-get install -y --no-install-recommends make && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock backend/Makefile ./
RUN make install


# Stage 3: Runtime — nginx + uvicorn under supervisord
FROM python:3.14-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /etc/nginx/sites-enabled/default

WORKDIR /app

COPY --from=backend-build /app/.venv /app/.venv
COPY backend/finance_tracker/ ./finance_tracker/
COPY backend/entrypoint.py ./

COPY --from=frontend-build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY supervisord.conf /etc/supervisor/conf.d/finance-tracker.conf

RUN mkdir -p /app/config /app/load_data

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    FT_CONFIG_DIR=/app/config \
    FT_LOAD_DATA_DIR=/app/load_data

EXPOSE 80

LABEL org.opencontainers.image.source="https://github.com/w0rmr1d3r/finance-tracker" \
      org.opencontainers.image.licenses="MIT"

CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
