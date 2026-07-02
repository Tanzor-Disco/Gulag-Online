# Gulag Online

A news aggregator that parses Telegram channels, stores posts in a database, and displays them on a website.

## Stack

* Backend: FastAPI, PostgreSQL (via Supabase, using the Supavisor connection pooler)
* Frontend: HTML, CSS, JavaScript (vanilla, infinite scroll via IntersectionObserver)
* Hosting: Render (backend), Supabase (database)
* Scheduling: an in-process background task, plus a GitHub Actions cron job hitting `/api/fetch`

## How It Works

* Telegram channels are parsed via their public web version at `t.me/s/<channel>`
* Parsing is triggered two ways: an in-process background task, and a secret-protected `/api/fetch` endpoint called on a schedule via GitHub Actions
* New posts are stored in PostgreSQL
* The website displays posts in an infinite-scroll feed, sorted by date, using `LIMIT`/`OFFSET` pagination

## Local Setup

```bash
python -m venv "putin_venv"
source ./putin_venv/bin/activate
pip install -r "requirements.txt"
```

Create a `.env` file in the project root:

```
URI=postgresql://user:password@host:port/dbname
FETCH_PARAM=your-secret-value
```

* `URI` — PostgreSQL connection string for your local database, e.g. `postgresql://postgres:password@localhost:5432/gulag_online`
* `FETCH_PARAM` — secret value required to trigger `/api/fetch`

Before running the server for the first time, make sure the database and the `posts` table exist. Either let the app create the table automatically (via `_create_table`, if implemented), or create it manually via `psql`:

```sql
CREATE TABLE posts (
    -- define columns here to match backend/db_manager.py
);
```

Run the server:

```bash
fastapi run ./backend/api.py
```

The server will be available at `http://localhost:8000`.

> Note: locally you'll need your own PostgreSQL instance (or point `URI` at a Supabase project) — the app no longer uses SQLite.

## Production

The live site: https://gulag-online.onrender.com/

The backend runs as a web service on Render, started via `fastapi run backend/api.py`, backed by a Supabase PostgreSQL database.

Note: Render's free tier spins down on inactivity, so the in-process background task doesn't run reliably while the service is asleep. The GitHub Actions cron job hitting `/api/fetch` exists as a workaround for that — it wakes the service and triggers a fetch even if the background task hasn't run.
