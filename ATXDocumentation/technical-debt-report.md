# Technical Debt Report

## 🎯 AWS Transformation Recommendation

### **RECOMMENDED TRANSFORMATIONS: None**

No AWS-managed transformation applies to this repository. The codebase is a Go + Python two-service application that does not use AWS SDKs, is not a Java/Node.js/Angular/.NET application requiring version upgrades, and has no matching criteria for any available transformation. Recommended next steps are to address the outdated `go-github` dependency and general code quality improvements documented below.

---

## Executive Summary

The modernisation-platform-slackbot is a relatively small, well-structured two-service application (Go API + Python Slackbot). The primary technical debt items are:

1. **Outdated `go-github` dependency** (v57, current is v68+) — Medium severity
2. **Duplicated code in Python slackbot** (checks_config loading duplicated) — Low severity
3. **Hardcoded repository path in Go commit package** — Low severity

## Prioritized Issues

| Priority | Category | Component | Issue | Severity |
|----------|----------|-----------|-------|----------|
| 1 | Outdated Dependency | API | `go-github` v57 (latest v68+) | Medium |
| 2 | Code Quality | Slackbot | Duplicated `CHECKS_CONFIG` loading block | Low |
| 3 | Code Quality | API | Hardcoded `/app/environments` path in commit package | Low |
| 4 | Code Quality | API | Error messages contain typo "ammend" (should be "amend") | Low |

## Detailed Findings

### Outdated Dependencies (Medium)

| Dependency | Current Version | Latest Available | Risk |
|------------|----------------|-----------------|------|
| `github.com/google/go-github/v57` | v57.0.0 | v68+ | Medium — missing newer GitHub API features and security patches |
| `slack-bolt` | 1.23.0 | Current | Low — recent version |
| `requests` | 2.32.3 | Current | Low — recent version |

### Code Quality Issues (Low)

1. **Duplicated config loading** in `slackbot/app.py`: Lines loading `CHECKS_CONFIG_PATH` and parsing the JSON appear twice
2. **Hardcoded path** `/app/environments` in `api/commit/commit.go` — tightly couples to container filesystem
3. **No graceful shutdown** handling in either service
4. **`retrigger_checks` route returns status code 0** on error instead of proper HTTP error codes

## Navigation

- [Detailed Technical Debt Summary](technical-debt/summary.md)
- [Outdated Components Analysis](technical-debt/outdated-components.md)
- [Maintenance Burden](technical-debt/maintenance-burden.md)
- [Remediation Plan](technical-debt/remediation-plan.md)
