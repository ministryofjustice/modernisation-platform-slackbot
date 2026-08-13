# Project Overview

## Purpose

The modernisation-platform-slackbot increases visibility of pull request check status for teams using the Ministry of Justice Modernisation Platform. It surfaces GitHub check results directly into Slack channels with emoji reactions and threaded replies.

## Organization

- **Owner**: Ministry of Justice (UK) — Modernisation Platform team
- **Repository**: `ministryofjustice/modernisation-platform-slackbot`

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| API Runtime | Go | 1.25 |
| API Framework | Gin | v1.10.1 |
| Slackbot Runtime | Python | 3.12 |
| Slackbot Framework | Slack Bolt | 1.23.0 |
| Container Orchestration | Kubernetes | Cloud Platform |
| Packaging | Helm | Chart API v2 |
| Container Registry | Amazon ECR | - |
| CI/CD | GitHub Actions | - |

## Services

### 1. Go API Service (`api/`)
HTTP service built with the Gin web framework that:
- Queries the GitHub API for PR check run statuses
- Evaluates check completion, failure, and pending states
- Provides a retrigger-checks endpoint to push empty commits to re-run CI

### 2. Python Slackbot (`slackbot/`)
Slack Bolt application running in Socket Mode that:
- Monitors a Slack channel for messages containing PR links
- Calls the Go API to get check status
- Adds emoji reactions (sparkles for success, x for failure, hourglass for pending)
- Posts threaded replies with check details
- Retries after a delay for recently-started checks

## Deployment Model

- Deployed to Kubernetes on the Cloud Platform (`apps.live.cloud-platform.service.justice.gov.uk`)
- Two environments: Development (1 replica, Recreate strategy) and Production (2 replicas, RollingUpdate)
- Docker images pushed to Amazon ECR
- Secrets managed via Kubernetes Secrets

## Source Code Metrics

- Total source lines: ~2,000
- Go files: 14 (including 4 test files)
- Python files: 1
- Configuration files: ~10 (YAML, JSON, Dockerfile)
