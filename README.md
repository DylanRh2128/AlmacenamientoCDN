# Private File Storage API

> Also reachable at `/storage` through this portfolio's `portfolio-gateway` reverse proxy,
> which puts all the portfolio's APIs behind one public URL.

## Problem

A business needs to store images and PDFs (invoices, product photos, ID documents) somewhere
that isn't publicly reachable, but still wants fast, CDN-backed delivery when a file is
actually needed.

## Solution

Upload an image or PDF (up to 10MB) and it's stored in a private AWS S3 bucket — never
publicly accessible. To download a file, you request a short-lived (10 minute) signed
CloudFront URL; anyone with that URL can fetch the file until it expires, but nobody can
generate the URL without an API key. See [docs/architecture.md](docs/architecture.md) for the
full reasoning.

## Stack

Python + FastAPI + PostgreSQL (SQLAlchemy, file metadata) + AWS S3 (storage) + CloudFront
(signed-URL CDN delivery).

## How to run it

```bash
python -m venv .venv
.venv/Scripts/activate        # or source .venv/bin/activate on Linux/Mac
pip install -r requirements.txt

cp .env.example .env          # fill in DATABASE_URL, API_KEY, and the AWS/CloudFront variables
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive API docs.

**Before this works against real AWS**, you need a private S3 bucket, a CloudFront
distribution with Origin Access Control, and a CloudFront key pair for signing URLs — see the
setup checklist in [docs/security.md](docs/security.md). Until then, you can still run the test
suite (everything is mocked) and explore the API shape.

## Run it with Docker

```bash
docker compose up --build
```

(pass the same AWS/CloudFront env vars as above; see [docs/deployment.md](docs/deployment.md))
The API is on `http://localhost:8003`.

## Try it

```bash
curl -X POST http://localhost:8000/files \
  -H "X-API-Key: your-api-key" \
  -F "file=@photo.jpg;type=image/jpeg"

curl http://localhost:8000/files/1/download-url -H "X-API-Key: your-api-key"
```

## Documentation

- [docs/architecture.md](docs/architecture.md) — AWS vs. Cloudflare R2, magic-byte validation, junior-acceptable vs. what a senior would do differently
- [docs/api-reference.md](docs/api-reference.md) — endpoints
- [docs/data-model.md](docs/data-model.md) — database schema
- [docs/security.md](docs/security.md) — AWS setup checklist, secrets handling
- [docs/testing.md](docs/testing.md) — what's tested and why
- [docs/deployment.md](docs/deployment.md) — Docker
