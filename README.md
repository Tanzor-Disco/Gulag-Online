# Gulag Online

A news aggregator that parses Telegram channels, stores posts in a database, and displays them on a website.

## Stack

- **Backend:** FastAPI, SQLite
- **Frontend:** HTML, CSS, JavaScript

## Setup and Run

```bash
python -m venv "putin_venv"
source ./putin_venv/bin/activate
pip install -r "requirements.txt"
fastapi run ./backend/api.py
```

The server will be available at `http://localhost:8000`.

## How It Works

- A background task periodically parses the configured Telegram channels (via the public web version at `t.me/s/<channel>`)
- New posts are stored in SQLite
- The website displays posts in a feed, sorted by date

