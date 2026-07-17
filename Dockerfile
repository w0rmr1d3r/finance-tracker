# Stage 1: Build frontend (Vite -> dist/)
FROM node:20-alpine@sha256:fb4cd12c85ee03686f6af5362a0b0d56d50c58a04632e6c0fb8363f609372293 AS frontend-build

WORKDIR /app
RUN apk add --no-cache make

COPY frontend/package-lock.json frontend/package.json frontend/Makefile ./
RUN make install

COPY frontend/ ./
RUN make build

# Stage 2: Declare uv to be reused later
FROM ghcr.io/astral-sh/uv:0.11.29@sha256:eb2843a1e56fd9e30c7276ce1a52cba86e64c7b385f5e3279a0e08e02dd058fc AS uv

# Stage 3: Build backend dependencies
FROM python:3.14-slim@sha256:d3400aa122fa42cf0af0dbe8ec3091b047eac5c8f7e3539f7135e86d855dc015 AS backend-build

COPY --from=uv /uv /bin/uv

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends make && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock backend/Makefile ./
RUN make install


# Stage 4: Runtime — nginx + uvicorn under supervisord
FROM python:3.14-slim@sha256:d3400aa122fa42cf0af0dbe8ec3091b047eac5c8f7e3539f7135e86d855dc015

RUN apt-get update && \
    apt-get upgrade -y && \
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
