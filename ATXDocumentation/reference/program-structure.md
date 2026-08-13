# Program Structure

## Repository Layout

```
modernisation-platform-slackbot/
├── api/                          # Go API service
│   ├── main.go                   # Entry point
│   ├── go.mod                    # Go module definition
│   ├── go.sum                    # Dependency checksums
│   ├── Dockerfile                # Multi-stage build (scratch)
│   ├── docker-test.yaml          # Test Docker config
│   ├── commit/
│   │   └── commit.go            # Git operations (clone, fetch, checkout, push)
│   ├── init_app/
│   │   ├── init_app.go          # Gin initialization
│   │   ├── init_commit.go       # Repository initialization
│   │   ├── init_env_vars.go     # Environment variable loading
│   │   └── init_gh.go           # GitHub client initialization
│   ├── pull_requests/
│   │   ├── check_pr.go          # PR status checking logic
│   │   ├── check_pr_test.go     # Tests for check_pr
│   │   ├── complete_check.go    # Completed check evaluation
│   │   ├── complete_check_test.go # Tests
│   │   ├── none_completed_check.go # In-progress/queued check evaluation
│   │   └── none_completed_check_test.go # Tests
│   ├── routes/
│   │   ├── init.go              # Route registration and logger
│   │   ├── check_pr.go         # /check-pr endpoint handler
│   │   └── retrigger_checks.go # /retrigger-checks endpoint handler
│   └── utils/
│       ├── github_data.go       # GitHub struct definition
│       ├── response.go          # HTTP response helper
│       ├── response_test.go     # Tests
│       └── time_since.go        # Time calculation utility
├── slackbot/                     # Python Slackbot service
│   ├── app.py                   # Entry point and all logic
│   ├── checks_config.json       # Check name patterns
│   ├── Dockerfile               # Python Alpine build
│   └── requirements.txt         # Python dependencies
├── deploy/                       # Helm chart
│   ├── Chart.yaml               # Chart metadata
│   ├── values.yaml              # Default values
│   ├── values-development.yaml  # Dev overrides
│   ├── values-production.yaml   # Prod overrides
│   └── templates/
│       ├── app.yaml             # Deployments (api + slackbot)
│       ├── app-svc.yaml         # Services
│       └── app-ing.yaml         # Ingress
├── docker-compose.yml            # Local development stack
├── README.md                     # Project documentation
└── .github/
    ├── dependabot.yml            # Automated dependency updates
    └── workflows/
        ├── build-deploy.yaml     # Main CI/CD pipeline
        ├── reusable-build-and-deploy.yaml # Reusable deploy job
        ├── code-analysis.yaml    # CodeQL analysis
        └── dependency-review.yml # Dependency vulnerability check
```

## Package Hierarchy (Go)

```
github.com/ministryofjustice/modernisation-platform-slackbot
├── main (package main)
├── commit (package commit)
├── init_app (package init_app)
├── pull_requests (package pull_requests)
├── routes (package routes)
└── utils (package utils)
```

## Cross-References

- [Modules](modules.md)
- [Components](../architecture/components.md)
