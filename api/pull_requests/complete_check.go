package pull_requests

import (
	"github.com/google/go-github/v57/github"
)

func CompletedCheck(check *github.CheckRun, prStatus []InvalidChecks) []InvalidChecks {
	name := ""
	if check.Name != nil {
		name = *check.Name
	}
	url := check.GetHTMLURL()

	switch *check.Conclusion {
	case "success", "skipped":
		// check passed or was intentionally skipped — not an invalid state, omit from results
	case "failure":
		prStatus = append(prStatus, InvalidChecks{name, "this check failed, check your pr and ammend", Failure, 0, url})
	case "action_required":
		prStatus = append(prStatus, InvalidChecks{name, "this check failed because an action is required, check your pr and ammend", Failure, 0, url})
	case "cancelled":
		prStatus = append(prStatus, InvalidChecks{name, "this check failed because somebody manually cancelled the check", Failure, 0, url})
	case "timed_out":
		prStatus = append(prStatus, InvalidChecks{name, "this check failed because it timed out", Failure, 0, url})
	case "stale":
		prStatus = append(prStatus, InvalidChecks{name, "this check failed because it was stale", Failure, 0, url})
	default:
		prStatus = append(prStatus, InvalidChecks{name, "unaccounted for state conclusion: " + *check.Conclusion, Failure, 0, url})
	}

	return prStatus
}
