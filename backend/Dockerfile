FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --frozen

COPY finance_tracker/ finance_tracker/
COPY entrypoint.py .

RUN mkdir -p load/entries_files/revolut load/entries_files/santander load/categories saved_files

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

LABEL org.opencontainers.image.source=https://github.com/w0rmr1d3r/finance-tracker/tree/main/backend \
      org.opencontainers.image.licenses=MIT

CMD ["python", "entrypoint.py"]
