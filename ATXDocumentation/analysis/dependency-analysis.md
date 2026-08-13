# Dependency Analysis

## Internal Dependencies

### Go Package Dependency Graph

```
main ──▶ init_app ──▶ routes ──▶ pull_requests ──▶ utils
                 │         │                          ▲
                 │         └──▶ commit                │
                 │         └──▶ utils ────────────────┘
                 └──▶ commit
                 └──▶ utils
```

**Dependency depth**: 4 levels (main → init_app → routes → pull_requests → utils)

### Service Dependency Graph

```
Slackbot ──HTTP──▶ API ──REST──▶ GitHub API
    │                    │
    │                    └──Git──▶ Target Repository
    └──WebSocket──▶ Slack API
```

## External Dependency Analysis

### Critical Dependencies (runtime-essential)

| Dependency | Criticality | Alternatives |
|------------|-------------|-------------|
| `gin` | High — web framework | Echo, Chi, stdlib net/http |
| `go-github` | High — core functionality | Manual HTTP calls |
| `go-git` | High — retrigger feature | shell out to git CLI |
| `slack-bolt` | High — core functionality | slack-sdk, manual WebSocket |
| `requests` | Medium — HTTP client | httpx, urllib3 |
| `oauth2` | Medium — authentication | Manual token header |

### Development Dependencies

| Dependency | Purpose |
|------------|---------|
| `testify` | Test assertions |
| `zap` + `gin-contrib/zap` | Structured logging |

### Transitive Dependency Count

- Go: 7 direct + ~35 indirect = ~42 total
- Python: 2 direct (slack-bolt pulls in its own dependencies)

## Dependency Health

| Metric | Assessment |
|--------|-----------|
| Outdated direct deps | 1 (go-github v57) |
| Known vulnerabilities | None detected |
| Dependency freshness | Good (most at latest) |
| License compatibility | All permissive (MIT, Apache 2.0, BSD) |
| Automated updates | Yes (Dependabot configured) |

## Supply Chain Security

- Dependabot configured for automated PR creation
- Dependency review workflow blocks critical vulnerabilities on PRs
- Go module checksums verified via `go.sum`
- Python dependencies pinned to exact versions

## Cross-References

- [Dependencies](../architecture/dependencies.md)
- [Outdated Components](../technical-debt/outdated-components.md)
