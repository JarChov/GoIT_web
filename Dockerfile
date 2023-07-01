FROM python:3.9

COPY . /app
WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/

RUN poetry install

CMD ["poetry", "run", "python", "book_assistant.py"]