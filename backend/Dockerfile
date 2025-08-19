FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install poetry && poetry install --no-root

COPY ./src /app/

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]