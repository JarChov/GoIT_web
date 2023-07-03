FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock /app/

RUN poetry install

CMD ["poetry", "run", "python", "web_hw_1_2/book_assistant.py"]