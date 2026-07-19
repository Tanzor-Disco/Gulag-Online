# Gulag Online

A news aggregator that parses Telegram channels, stores posts in a PostgreSQL database, and displays them on a website.

## Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL (Supabase)
- **Frontend:** HTML, CSS, JavaScript (vanilla, infinite scroll via `IntersectionObserver`)
- **Containerization:** Docker
- **Hosting:** Render (backend), Supabase (database)
- **Automation:** GitHub Actions (scheduled fetches)

## How It Works

- Telegram channels are parsed through their public web pages (`t.me/s/<channel>`).
- New posts are stored in PostgreSQL.
- The website displays posts in an infinite-scroll feed using `LIMIT`/`OFFSET` pagination.
- Fetching can be triggered manually through the protected `/api/fetch` endpoint or automatically by a scheduled GitHub Actions workflow.

## Local Setup (Docker)

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd gulag-online
```

Create a `.env` file in the project root:

```env
URI=postgresql://user:password@host:port/database
FETCH_PARAM=your-secret-value
```

- `URI` — PostgreSQL connection string.
- `FETCH_PARAM` — an arbitrary secret value used to protect the `/api/fetch` endpoint. It is required by the GitHub Actions workflow and when triggering the endpoint manually with `curl`.

Build the Docker image:

```bash
docker buildx build -t gulag-online .
```

Run the container:

```bash
docker run --rm -it --env-file .env -p 8000:8000 gulag-online
```

The application will be available at:

```
http://localhost:8000
```

## Production

Live website:

https://gulag-online.onrender.com

The application is deployed on Render and uses a Supabase PostgreSQL database.

Render's free tier suspends inactive services, so scheduled fetching is handled by a GitHub Actions workflow that periodically calls the protected `/api/fetch` endpoint.
