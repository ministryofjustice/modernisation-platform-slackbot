# System Overview

## Architecture Style

The system follows a **two-service microservice architecture** with clear separation of concerns:

- **API Service** (Go): Stateless HTTP service responsible for GitHub API interactions
- **Slackbot Service** (Python): Event-driven service responsible for Slack channel monitoring and message reactions

## Technology Stack

### API Service
- **Language**: Go 1.25
- **Web Framework**: Gin v1.10.1
- **GitHub Client**: go-github v57
- **Git Operations**: go-git v5.16.2
- **Logging**: Uber Zap + gin-contrib/zap
- **Auth**: OAuth2 (GitHub personal access token)

### Slackbot Service
- **Language**: Python 3.12
- **Framework**: Slack Bolt 1.23.0 (Socket Mode)
- **HTTP Client**: requests 2.32.3

### Infrastructure
- **Container Runtime**: Docker (multi-stage builds)
- **Orchestration**: Kubernetes (Helm chart)
- **Registry**: Amazon ECR
- **CI/CD**: GitHub Actions
- **Ingress**: Kubernetes Ingress with external-dns

## Deployment Architecture

```
┌─────────────────────────────────────────────────┐
│           Kubernetes Cluster                     │
│         (Cloud Platform)                         │
│                                                  │
│  ┌──────────────┐     ┌──────────────────┐      │
│  │  Slackbot    │────▶│   API Service    │      │
│  │  (Python)    │     │   (Go/Gin)       │      │
│  │  Socket Mode │     │   Port 3000      │      │
│  └──────────────┘     └────────┬─────────┘      │
│                                │                 │
└────────────────────────────────┼─────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   GitHub API            │
                    │   (Check Runs,          │
                    │    Pull Requests)       │
                    └────────────────────────-┘
```

## Key Architectural Decisions

1. **Socket Mode for Slack**: Uses Slack Socket Mode rather than HTTP webhooks, eliminating the need for a public-facing endpoint for the slackbot
2. **Separate Services**: API and Slackbot are separate containers/deployments allowing independent scaling and deployment
3. **Scratch Container for API**: Go binary runs in a `scratch` container for minimal attack surface
4. **Git Clone for Retrigger**: The API clones the target repository to push empty commits for retriggering checks

## Cross-References

- [Components](components.md)
- [Dependencies](dependencies.md)
- [Deployment Diagrams](../diagrams/architecture/)
