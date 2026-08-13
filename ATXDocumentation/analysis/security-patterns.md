# Security Patterns

## Authentication

### GitHub API Authentication
- OAuth2 static token source using personal access token
- Token stored in Kubernetes Secret, injected via environment variable
- Token validated at startup (empty check)

### Slack Authentication
- Three-token model: Bot Token, App Token, Signing Secret
- All stored in Kubernetes Secrets
- Socket Mode eliminates need for public webhook endpoints

### Git Push Authentication
- HTTP Basic Auth with username + token
- Force-with-lease prevents accidental force pushes

## Container Security

### API Service (Go)
- Multi-stage build: `golang:1.25.2-alpine3.22` → `scratch`
- Final image has no shell, no OS, minimal attack surface
- Runs as non-root user (UID 1000)
- CA certificates explicitly copied for HTTPS

### Slackbot Service (Python)
- Base: `python:3.12-alpine3.21`
- Runs as non-root user (UID 1000)
- No unnecessary packages installed

### Kubernetes Security Context
```yaml
securityContext:
  allowPrivilegeEscalation: false
  seccompProfile:
    type: RuntimeDefault
  capabilities:
    drop:
      - ALL
  runAsNonRoot: true
```

## Network Security

- Ingress with TLS termination
- Internal service communication on cluster network (api:3000)
- Slackbot uses Socket Mode (outbound WebSocket) — no inbound connections needed
- External-dns for DNS management

## Secrets Management

All sensitive values stored as Kubernetes Secrets:
- `github-token`
- `github-url`
- `github-user`
- `slack-bot-token`
- `slack-signing-secret`
- `slack-app-token`
- `slack-channel-id`
- `api-url`

## CI/CD Security

- CodeQL static analysis on PRs
- Dependency review blocks critical vulnerabilities
- Environment-based deployment approvals
- Separate development and production environments

## Potential Security Considerations

1. **No rate limiting** on API endpoints — could be abused to exhaust GitHub API quota
2. **No input validation** on PR ID parameter (relies on GitHub API to reject invalid values)
3. **Git credentials in memory** — token passed through function parameters
4. **No request authentication** on the Go API — any pod in the cluster can call it

## Cross-References

- [Error Handling](../behavior/error-handling.md)
- [System Overview](../architecture/system-overview.md)
