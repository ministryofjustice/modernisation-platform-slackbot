# Slackbot

This directory contains the Python Slack bot service for cloud-platform-hammer-bot.

## Purpose

The Slack bot listens for pull request links posted in Slack, calls the API service to inspect check status, and then reacts to the message or posts a threaded reply.

## Runtime

- Python 3.12
- `slack-bolt`
- `requests`

## Build

For local development, create a `.env` file in the repository root with the variables documented in [../README.md](../README.md).

Then build or start the Slack bot from the repository root with Docker Compose:

```sh
docker compose build slackbot
docker compose up slackbot
```

These commands should be run from the repository root.

The Slack bot expects these environment variables:

- `SLACK_BOT_TOKEN`
- `SLACK_SIGNING_SECRET`
- `SLACK_APP_TOKEN`
- `GITHUB_URL`
- `API_URL` (optional, defaults to `http://api:3000`)

For local development with Docker Compose, those variables are typically supplied through the repository root `.env` file.

If you want to run the Slack bot container outside Compose, export the required variables in your shell first and then run:

```sh
./slackbot/run_docker.sh
```

## Dependencies

Python dependencies are defined in [requirements.txt](requirements.txt).

## Files

- [app.py](app.py): main Slack bot implementation
- [Dockerfile](Dockerfile): container image definition
- [run_docker.sh](run_docker.sh): local container run helper that uses exported environment variables

## Configuring workflow checks

The set of workflow checks that the Slack bot watches is defined in [checks_config.json](checks_config.json).

- Each top-level key represents a check category (for example, `plan`, `static_analysis`).
- Under each category, `name_patterns` is an array of regular expressions that are matched (case-insensitively) against the GitHub check `Name` field.
- Any check whose name matches one or more configured patterns is treated as a "configured" check for the purposes of failure and pending-status notifications.

To change which checks are monitored:

1. Edit [checks_config.json](checks_config.json) to add, remove, or update `name_patterns` entries.
2. Rebuild and restart the Slack bot container (for example, from the repository root: `docker compose build slackbot && docker compose up slackbot`).

The bot will then use the updated configuration for all subsequent pull request messages.