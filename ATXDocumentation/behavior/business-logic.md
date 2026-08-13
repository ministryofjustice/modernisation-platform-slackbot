> ⚠️ **Early Access**: Behavior documentation is in early access. Please review critically.

# Business Logic

## API Service Business Logic

### PR Check Status Evaluation (`pull_requests/check_pr.go`)

The core business logic evaluates GitHub check runs and categorizes them:

**Status Enum:**
- `Success` (0) — Check passed
- `Failure` (1) — Check failed
- `Pending` (2) — Check still running or queued

**Rules for completed checks** (`complete_check.go`):
- `success` or `skipped` → Not reported (valid state)
- `failure` → Reported as Failure with "check your pr and amend"
- `action_required` → Reported as Failure
- `cancelled` → Reported as Failure (manually cancelled)
- `timed_out` → Reported as Failure
- `stale` → Reported as Failure
- Any other conclusion → Reported as Failure with "unaccounted for state"

**Rules for in-progress checks** (`none_completed_check.go`):
- Started < 10 minutes ago → Pending with retry duration
- Started >= 10 minutes ago → Pending with no retry (something wrong)

**Rules for queued checks** (`none_completed_check.go`):
- Queued < 10 minutes → Pending with retry duration
- Queued >= 10 minutes → Pending with no retry (something wrong)

### Combined Status Evaluation (`check_pr.go:CheckCombinedStatus`)
- If combined state is `pending` → evaluate via `CheckPendingStatus`
- If individual status is `failure` → report as failure
- If individual status is `success` → skip

### Retrigger Logic (`commit/commit.go`)
1. Open or clone the target repository
2. Fetch the specified branch
3. Force-checkout the branch
4. Create an empty commit ("Hammer-bot blank commit")
5. Push with force-with-lease to the branch

## Slackbot Business Logic

### Message Pattern Matching
- Monitors channel for messages containing the configured repository's pull request URLs
- Extracts PR ID(s) from the URL pattern `/pull/(\d+)`

### Check Categorization (`checks_config.json`)
Checks are categorized by name patterns:
- `plan`: patterns `^plan`, `/ plan$`
- `static_analysis`: "Terraform Static Analysis"
- `linting`: "TFLint Scan"
- `security_scanning`: "Checkov Scan"
- `policy_validation`: "run-opa-policy-tests"
- `binary_file_check`: "Check for Binary and Archive Files"

### Reaction Logic
Only **configured** checks (matching patterns above) trigger reactions:
- All configured checks pass → ✨ (sparkles) emoji
- Any configured check failed → ❌ (x) emoji + threaded summary
- Recent pending configured checks → 🔄 (repeat) emoji + retry timer
- Old pending queued checks (>10min, "queued") → ⏳ (hourglass) + warning message
- Still pending after retry → ⏳ + ⚠️ + team notification

## Cross-References

- [Decision Logic](decision-logic.md)
- [Workflows](workflows.md)
- [Components](../architecture/components.md)
