# Dependencies

## Internal Component Dependencies

```
main.go
├── init_app/
│   ├── init_env_vars.go (os)
│   ├── init_gh.go (go-github, oauth2)
│   ├── init_commit.go (commit/, go-git)
│   └── init_app.go (routes/, utils/)
├── routes/
│   ├── init.go (gin, zap, utils/)
│   ├── check_pr.go (gin, go-github, pull_requests/, utils/)
│   └── retrigger_checks.go (gin, commit/, utils/)
├── pull_requests/
│   ├── check_pr.go (gin, go-github, utils/)
│   ├── complete_check.go (go-github)
│   └── none_completed_check.go (go-github, utils/)
├── commit/
│   └── commit.go (go-git)
└── utils/
    ├── github_data.go (go-git, go-github)
    ├── response.go (gin)
    └── time_since.go (time)
```

## External Dependencies — Go API

### Direct Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `github.com/gin-gonic/gin` | v1.10.1 | HTTP web framework |
| `github.com/gin-contrib/zap` | v1.1.5 | Zap logging middleware for Gin |
| `github.com/go-git/go-git/v5` | v5.16.2 | Pure Go git implementation |
| `github.com/google/go-github/v57` | v57.0.0 | GitHub API v3 client |
| `github.com/stretchr/testify` | v1.10.0 | Test assertions (dev) |
| `go.uber.org/zap` | v1.27.0 | Structured logging |
| `golang.org/x/oauth2` | v0.30.0 | OAuth2 client for GitHub auth |

### Key Indirect Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `github.com/ProtonMail/go-crypto` | v1.1.6 | Cryptographic operations for git |
| `github.com/cloudflare/circl` | v1.6.1 | Cryptographic library |
| `golang.org/x/crypto` | v0.37.0 | Extended crypto primitives |
| `golang.org/x/net` | v0.39.0 | Network utilities |
| `google.golang.org/protobuf` | v1.36.6 | Protocol Buffers |

## External Dependencies — Python Slackbot

| Package | Version | Purpose |
|---------|---------|---------|
| `slack-bolt` | 1.23.0 | Slack app framework (Socket Mode) |
| `requests` | 2.32.3 | HTTP client for API calls |

## External Services

| Service | Usage | Authentication |
|---------|-------|---------------|
| GitHub API v3 | Check runs, PR data, combined status | Personal Access Token (OAuth2) |
| Slack API | Socket Mode, reactions, messages | Bot Token + App Token + Signing Secret |
| Amazon ECR | Container image storage | AWS IAM (CI/CD) |

## Dependency Graph (Service-to-Service)

```
Slack (WebSocket) ──▶ Slackbot (Python)
                          │
                          │ HTTP GET /check-pr
                          ▼
                     API (Go/Gin)
                          │
                          │ REST API
                          ▼
                     GitHub API v3
```

## Cross-References

- [Dependency Analysis](../analysis/dependency-analysis.md)
- [Outdated Components](../technical-debt/outdated-components.md)
