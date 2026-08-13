# Validation Criteria

## Migration Success Criteria

### 1. Functional Parity

| Criterion | Validation Method |
|-----------|------------------|
| API returns correct check statuses | Existing Go unit tests pass |
| API health endpoint responds | `GET /healthz` returns 200 |
| Slackbot detects PR URLs | Manual test with PR link in channel |
| Slackbot adds correct emoji | Observe sparkles/x/hourglass |
| Slackbot posts thread replies | Observe threaded message |
| Retry mechanism works | Post PR with pending checks, observe delayed retry |
| Retrigger endpoint works | Call `/retrigger-checks/:branch`, verify commit pushed |

### 2. Non-Functional Requirements

| Criterion | Threshold |
|-----------|-----------|
| API startup time | Container ready within probe window (30s × 10 attempts) |
| API response time | < 5s for check-pr (dependent on GitHub API) |
| Memory usage (API) | Within 2Gi limit |
| Memory usage (Slackbot) | Within 512Mi limit |
| Container runs as non-root | UID != 0 |
| No privilege escalation | `allowPrivilegeEscalation: false` |

### 3. Deployment Validation

| Criterion | Validation |
|-----------|-----------|
| Docker images build | CI pipeline succeeds |
| Images push to ECR | Push step completes |
| Helm deployment succeeds | `helm upgrade` exits 0 |
| Pods reach Ready state | `kubectl get pods` shows Running |
| Ingress routes traffic | External URL responds with 200 |
| Development env works | Dev deployment approval + successful deploy |
| Production env works | Prod deployment approval + successful deploy |

### 4. Security Validation

| Criterion | Validation |
|-----------|-----------|
| No hardcoded secrets | Code review / secret scanning |
| Secrets injected via K8s | Pod env vars from SecretKeyRef |
| Container security context | seccomp + drop ALL + non-root |
| Dependency vulnerabilities | Dependency review workflow passes |
| Static analysis | CodeQL workflow passes |

### 5. Test Suite Validation

| Criterion | Validation |
|-----------|-----------|
| All existing tests pass | `go test -race ./...` exits 0 |
| Tests pass on multiple OS | Ubuntu + macOS matrix green |
| Linting passes | `golangci-lint` + `gofumpt` clean |

## Cross-References

- [Test Specifications](test-specifications.md)
- [Component Order](component-order.md)
