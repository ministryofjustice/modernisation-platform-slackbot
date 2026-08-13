# Remediation Plan

## Prioritized Action Items

### Priority 1: Upgrade go-github (Medium Severity)

**Current**: v57.0.0  
**Target**: Latest stable (v68+)  
**Effort**: Medium complexity  
**Risk**: Medium — breaking API changes between major versions

**Steps**:
1. Update `go.mod` to reference the latest `go-github` major version
2. Review the changelog for breaking changes between v57 and target version
3. Update import paths (major version is part of the import path in Go modules)
4. Fix any compilation errors from API changes
5. Run existing test suite to validate behavior
6. Test against live GitHub API in development environment

### Priority 2: Fix Duplicated Config Loading (Low Severity)

**Location**: `slackbot/app.py`  
**Effort**: Low complexity  

**Steps**:
1. Remove the second `CHECKS_CONFIG_PATH` assignment and `json.load` block (lines are duplicated)
2. Verify the slackbot still starts correctly

### Priority 3: Fix Hardcoded Repository References (Low Severity)

**Location**: `api/pull_requests/check_pr.go` — `CheckPendingStatus` function  
**Effort**: Low complexity  

**Steps**:
1. Pass owner and repository as parameters to `CheckPendingStatus` instead of hardcoding
2. Update callers to provide the parsed values

### Priority 4: Fix HTTP Status Codes in Retrigger Endpoint (Low Severity)

**Location**: `api/routes/retrigger_checks.go`  
**Effort**: Low complexity  

**Steps**:
1. Replace `Status: 0` with proper HTTP status codes (e.g., `http.StatusInternalServerError`)
2. Add a success response at the end of the handler

### Priority 5: Fix Typos in Error Messages (Low Severity)

**Location**: `api/pull_requests/complete_check.go`  
**Effort**: Low complexity  

**Steps**:
1. Replace "ammend" with "amend" in user-facing messages

## Dependencies Between Items

```
Priority 1 (go-github upgrade) → Independent, can be done anytime
Priority 2 (config duplication) → Independent
Priority 3 (hardcoded refs) → Independent
Priority 4 (status codes) → Independent
Priority 5 (typos) → Independent
```

All items are independent and can be addressed in any order.

## Cross-References

- [Outdated Components](outdated-components.md)
- [Technical Debt Report](../technical-debt-report.md)
