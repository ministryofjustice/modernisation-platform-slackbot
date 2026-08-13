# Test Specifications

## Existing Tests

### Go Test Files

| Test File | Package | Functions Under Test |
|-----------|---------|---------------------|
| `pull_requests/check_pr_test.go` | `pull_requests` | `CheckPRStatus` |
| `pull_requests/complete_check_test.go` | `pull_requests` | `CompletedCheck` |
| `pull_requests/none_completed_check_test.go` | `pull_requests` | `InProgressCheck`, `QueuedCheck` |
| `utils/response_test.go` | `utils` | `SendResponse` |

### Test Patterns Used
- Table-driven tests (`tests := []struct{...}`)
- Mock time functions (injected `getTimeSince`)
- HTTP recorder (`httptest.NewRecorder`) for Gin context testing
- `testify/assert` for assertions

## Required Test Cases for Migration Validation

### API Service

#### Unit Tests (must pass)

| Component | Test Case | Expected Behavior |
|-----------|-----------|-------------------|
| `CheckPRStatus` | All checks completed and successful | Returns empty slice |
| `CheckPRStatus` | Mix of completed failures | Returns InvalidChecks with Failure status |
| `CheckPRStatus` | In-progress check < 10min | Returns Pending with RetryAfter > 0 |
| `CheckPRStatus` | In-progress check > 10min | Returns Pending with RetryAfter = 0 |
| `CheckPRStatus` | Queued check < 10min | Returns Pending with RetryAfter > 0 |
| `CheckPRStatus` | Queued check > 10min | Returns Pending with RetryAfter = 0 |
| `CompletedCheck` | Each conclusion type | Correct status and message |
| `SendResponse` | Message, Data, Error, Empty | Correct JSON output |
| `TimeSince` | Time < 10 min | Returns (true, duration, 10m) |
| `TimeSince` | Time >= 10 min | Returns (false, duration, 10m) |

#### Integration Tests (recommended for migration)

| Endpoint | Test Case | Expected |
|----------|-----------|----------|
| `GET /check-pr?id=1` | Valid PR with passing checks | 200, empty array |
| `GET /check-pr?id=1` | Valid PR with failures | 200, array with InvalidChecks |
| `GET /check-pr?id=1,2` | Multiple PRs | 200, results for each |
| `GET /healthz` | Health check | 200 |

### Slackbot Service

#### Functional Tests (recommended)

| Scenario | Input | Expected |
|----------|-------|----------|
| PR link message | Message with PR URL | API called with correct ID |
| All pass | API returns empty | Sparkles emoji added |
| Failure | API returns failure check | X emoji + thread reply |
| Pending recent | API returns pending with RetryAfter | Repeat emoji + timer scheduled |
| Non-matching message | Message without PR URL | No action taken |

## Cross-References

- [Validation Criteria](validation-criteria.md)
- [Code Metrics](../analysis/code-metrics.md)
