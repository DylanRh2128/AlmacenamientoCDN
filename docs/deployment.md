# Deployment

## Docker (local)

```bash
docker compose up --build
```

(with `API_KEY` and the AWS/CloudFront variables set in your shell or a `.env` next to
`docker-compose.yml`, which Docker Compose reads automatically)

Two containers: `api` (port `8003` on the host) and `db` (`postgres:16-alpine`, port `5542` on
the host, with a healthcheck `api` waits on). `DATABASE_URL` inside `docker-compose.yml` points
at `db:5432` by Docker network name, separate from the `localhost`-based value in
`.env.example`.

## Why Docker, no Kubernetes

Same reasoning as the rest of this portfolio: one service, one database — Kubernetes solves
problems (multi-replica rollout, cluster-wide self-healing) this single-container app doesn't
have.

## Deploying beyond local Docker

The `Dockerfile` is what a platform like Railway or Render would build directly. Set
`DATABASE_URL` (their managed Postgres) plus `API_KEY` and all the AWS/CloudFront variables as
environment variables in their dashboard — the AWS resources themselves (bucket, distribution,
IAM user, key pair) are the same regardless of where the API itself runs; see the checklist in
`docs/security.md`.
