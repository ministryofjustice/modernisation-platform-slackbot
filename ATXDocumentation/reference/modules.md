# Modules

## Go Modules

**Module path**: `github.com/ministryofjustice/modernisation-platform-slackbot`  
**Go version**: 1.25  
**Toolchain**: go1.25.1

### Package: `main` (`api/main.go`)
- Entry point; no exported symbols
- Dependencies: `init_app`, `utils`

### Package: `init_app` (`api/init_app/`)
- Application initialization
- Dependencies: `commit`, `routes`, `utils`, `gin`, `go-git`, `go-github`, `oauth2`

### Package: `routes` (`api/routes/`)
- HTTP route registration and handlers
- Dependencies: `commit`, `pull_requests`, `utils`, `gin`, `go-github`, `zap`, `gin-contrib/zap`

### Package: `pull_requests` (`api/pull_requests/`)
- Core business logic for PR check evaluation
- Dependencies: `utils`, `gin`, `go-github`

### Package: `commit` (`api/commit/`)
- Git operations (clone, fetch, checkout, push)
- Dependencies: `go-git`

### Package: `utils` (`api/utils/`)
- Shared utilities (response helpers, time calculations, GitHub struct)
- Dependencies: `gin`, `go-git`, `go-github`

## Python Modules

### Module: `app` (`slackbot/app.py`)
- Single-file application containing all slackbot logic
- Dependencies: `slack-bolt`, `requests`, standard library (`json`, `logging`, `os`, `re`, `threading`, `urllib.parse`, `typing`)

### Configuration: `checks_config.json`
- JSON configuration file defining check name patterns for categorization
- Loaded at module startup

## Module Dependency Flow

```
main
 └── init_app
      ├── commit
      ├── routes
      │    ├── commit
      │    ├── pull_requests
      │    │    └── utils
      │    └── utils
      └── utils
```

## Cross-References

- [Program Structure](program-structure.md)
- [Dependencies](../architecture/dependencies.md)
