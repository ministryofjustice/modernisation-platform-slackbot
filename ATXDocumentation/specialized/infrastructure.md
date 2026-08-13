# Specialized Documentation

## Infrastructure and Deployment Configuration

### Docker Compose (Local Development)

The `docker-compose.yml` defines the local development stack:

| Service | Build Context | Ports | Dependencies |
|---------|--------------|-------|-------------|
| `api` | `./api` | 3001:3000 | None |
| `slackbot` | `./slackbot` | 3000:3000 | `api` |

Environment variables are passed from a `.env` file in the repository root.

### Helm Chart Structure

```
deploy/
├── Chart.yaml              # apiVersion: v2, type: application
├── values.yaml             # Shared defaults
├── values-development.yaml # Dev overrides (1 replica, Recreate)
├── values-production.yaml  # Prod overrides (2 replicas, RollingUpdate)
└── templates/
    ├── app.yaml            # Deployments for both services
    ├── app-svc.yaml        # ClusterIP Services
    └── app-ing.yaml        # Ingress with TLS
```

### Kubernetes Resource Configuration

**API Deployment:**
- Startup probe: `GET /healthz` (30s period, 10 failures)
- Readiness probe: `GET /healthz` (60s initial, 60s period)
- Resources: 100m-500m CPU, 256Mi-2Gi memory

**Slackbot Deployment:**
- No probes (Socket Mode — no HTTP endpoint)
- Resources: 100m-300m CPU, 128Mi-512Mi memory

### CI/CD Pipeline

| Workflow | File | Purpose |
|----------|------|---------|
| Build & Deploy | `build-deploy.yaml` | Main pipeline: lint → test → deploy |
| Reusable B&D | `reusable-build-and-deploy.yaml` | Shared deploy logic |
| Code Analysis | `code-analysis.yaml` | CodeQL on PRs |
| Dependency Review | `dependency-review.yml` | Block vulnerable deps |

### Container Registry

- **Registry**: Amazon ECR
- **Image tagging**: Git SHA-based
- **Push trigger**: CI pipeline after tests pass

## Cross-References

- [System Overview](../architecture/system-overview.md)
- [Architecture Diagrams](../diagrams/architecture/system-context.md)
