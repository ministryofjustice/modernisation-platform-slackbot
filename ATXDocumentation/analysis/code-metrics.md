# Code Metrics

## Size Metrics

| Metric | Value |
|--------|-------|
| Total source lines (Go + Python + YAML) | ~2,000 |
| Go source files | 10 (excluding tests) |
| Go test files | 4 |
| Python source files | 1 |
| Configuration files (YAML/JSON) | ~10 |
| Dockerfiles | 2 |

## File-Level Metrics

### Go Files (by size, descending)
| File | Lines | Functions | Complexity |
|------|-------|-----------|-----------|
| `routes/check_pr.go` | ~60 | 1 (handler) | Medium |
| `commit/commit.go` | ~80 | 5 | Low |
| `pull_requests/check_pr.go` | ~90 | 4 | Medium |
| `pull_requests/none_completed_check.go` | ~35 | 2 | Low |
| `pull_requests/complete_check.go` | ~30 | 1 | Low |
| `routes/retrigger_checks.go` | ~40 | 1 | Low |
| `routes/init.go` | ~45 | 3 | Low |
| `utils/response.go` | ~25 | 1 | Low |
| `utils/time_since.go` | ~15 | 1 | Low |
| `utils/github_data.go` | ~12 | 0 | Low |

### Python Files
| File | Lines | Functions | Complexity |
|------|-------|-----------|-----------|
| `slackbot/app.py` | ~210 | 15 | Medium |

## Test Coverage

| Package | Test File | Functions Tested |
|---------|-----------|-----------------|
| `pull_requests` | `check_pr_test.go` | `CheckPRStatus` |
| `pull_requests` | `complete_check_test.go` | `CompletedCheck` |
| `pull_requests` | `none_completed_check_test.go` | `InProgressCheck`, `QueuedCheck` |
| `utils` | `response_test.go` | `SendResponse` |

**Notable gaps**: No tests for `routes`, `commit`, or `init_app` packages. No tests for the Python slackbot.

## Quality Indicators

| Indicator | Assessment |
|-----------|-----------|
| Code duplication | Low (one instance in Python slackbot) |
| Function length | Good (most functions < 30 lines) |
| Package cohesion | Good (clear separation of concerns) |
| Naming consistency | Good |
| Error handling coverage | Moderate (some gaps in retrigger endpoint) |

## Cross-References

- [Complexity Analysis](complexity-analysis.md)
- [Tech Debt](tech-debt.md)
