FROM python:3.13-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    POETRY_VIRTUALENVS_CREATE=false \
    APP_HOME=/app

WORKDIR $APP_HOME

COPY ../pyproject.toml poetry.lock $APP_HOME/

RUN apt-get update \
    && apt-get -y dist-upgrade \
    && apt-get install -y bash curl netcat-traditional gettext \
    && pip install poetry \
    && poetry install --no-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ../bot/ $APP_HOME/bot/

ENV PATH="/root/.local/bin:$PATH"

EXPOSE 8000

CMD ["python", "bot/main.py"]

