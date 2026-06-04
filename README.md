# modernisation-platform-slackbot

## Purpose

Increase visibility of pull request check status for teams using the Modernisation Platform, by surfacing GitHub check results directly into Slack.

## How it works

There are two components:

1. **[API](api/)** — a Go service that processes incoming Slack messages, looks up the status of pull request checks via the GitHub API, and returns results to the Slack bot.
2. **[Slackbot](slackbot/)** — a Python service (using Slack Bolt) that watches a Slack channel for relevant messages. When a result is received from the API it adds an emoji reaction to the message in the channel.

## Repository structure

```
api/          Go API service
slackbot/     Python Slack bot service
deploy/       Helm chart for Kubernetes deployment
.github/
  workflows/  GitHub Actions CI/CD workflows
```

## Local development

API-specific build and test commands live in [api/README.md](api/README.md).
Slack bot details live in [slackbot/README.md](slackbot/README.md).

Before starting the local stack, create a `.env` file in the repository root:

```dotenv
GITHUB_TOKEN=
GITHUB_URL=https://github.com/ministryofjustice/modernisation-platform-environments.git
GITHUB_USER=
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
SLACK_APP_TOKEN=
API_URL=http://api:3000
```

| Variable | Description | Where to obtain |
|---|---|---|
| `GITHUB_TOKEN` | Personal access token with access to the environments repository | GitHub Settings → Developer settings → Personal access tokens |
| `GITHUB_URL` | Repository URL used by the API and Slack bot for PR matching | Use `https://github.com/ministryofjustice/modernisation-platform-environments.git` |
| `GITHUB_USER` | GitHub username associated with `GITHUB_TOKEN` | Your GitHub profile |
| `SLACK_BOT_TOKEN` | Bot user OAuth token | Slack app → OAuth & Permissions |
| `SLACK_SIGNING_SECRET` | Signing secret for request verification | Slack app → Basic Information |
| `SLACK_APP_TOKEN` | App-level token for Socket Mode | Slack app → Basic Information → App-Level Tokens |
| `API_URL` | API base URL used by the Slack bot | Keep as `http://api:3000` for local Docker Compose |

Build and start the full stack from the repository root:

```sh
docker compose up --build
```

This starts both services defined in [docker-compose.yml](docker-compose.yml):

- API on `http://localhost:3001`
- Slack bot connected to the API via `http://api:3000`

To stop the stack:

```sh
docker compose down
```

To rebuild a single service:

```sh
docker compose build api
docker compose build slackbot
```

## GitHub Actions workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| [Build and Deploy](.github/workflows/build-deploy.yaml) | Pull request, push to `main`, manual | Validates code with staticcheck (lint), runs Go tests, builds Docker images, pushes to ECR, deploys to Kubernetes |
| [Reusable build and deploy](.github/workflows/reusable-build-and-deploy.yaml) | Called by build-deploy | Shared build and deploy logic for all environments |
| [Code quality tests](.github/workflows/code-analysis.yaml) | Pull request to `main` | Runs CodeQL static analysis on the Go codebase |
| [Dependency review](.github/workflows/dependency-review.yml) | Pull request to `main` | Blocks critical severity dependency vulnerabilities |

### Deployment pipeline

The build-deploy workflow runs jobs in sequence: lint first (fail-fast), then tests, then deployment.

```
Pull request / push to main
        │
        ▼
  Lint (staticcheck) → Run tests (go-test)
        │
        ▼
  Deploy → development
        │  (must succeed)
        ▼
  Deploy → production  ← requires environment approval + main branch only
```

**Job execution order:**

1. **staticcheck** (runs first, no dependencies)
   - Installs and runs `gofumpt` formatting check
   - Runs `golangci-lint` for code quality

2. **go-test** (depends on staticcheck)
   - Runs on `ubuntu-latest` and `macos-latest` matrix
   - Runs `go test -race` with coverage reporting
   - Uploads coverage to Codecov (Ubuntu only to avoid duplicates)
   - Uploads test logs as artifacts

3. **deploy-development** (depends on both lint and test jobs)
   - Deploys on every pull request or push to `main`
   - For manual runs, a target branch can be specified via the `development_branch` input

4. **deploy-production** (conditional: main branch only)
   - Runs only when the ref is `main`, after development succeeds
   - Requires approval configured on the `production` GitHub environment

## Helm chart

The Kubernetes deployment is managed by the Helm chart in [deploy/](deploy/).

Values are layered in order:

1. [deploy/values.yaml](deploy/values.yaml) — shared defaults for all environments
2. `deploy/values-<environment>.yaml` — environment-specific overrides

| Parameter | Development | Production |
|---|---|---|
| `api.replicas` | 1 | 2 |
| `slackbot.replicas` | 1 | 2 |
| `deploymentStrategy.type` | `Recreate` | `RollingUpdate` |
| `slackbot.environment` | `development` | `production` |

Runtime values (ECR URL, image tags, namespace, ingress identifier) are passed at deploy time via `--set-string` from the workflow.

