# API

This directory contains the Go API service for cloud-platform-hammer-bot.

## Build

For local development, create a `.env` file in the repository root with the variables documented in [../README.md](../README.md).

Then build or start the API from the repository root with Docker Compose:

```sh
docker compose build api
docker compose up api
```

These commands should be run from the repository root.

## Test

Run the Go test suite from inside this directory:

```sh
go test ./...
```

## Run

The service expects these environment variables:

- `GITHUB_TOKEN`
- `GITHUB_URL`
- `GITHUB_USER`
- `GIN_MODE` (optional, defaults to `debug`)

For local development with Docker Compose, those variables are typically supplied through the repository root `.env` file.

The HTTP server listens on port `3000`.