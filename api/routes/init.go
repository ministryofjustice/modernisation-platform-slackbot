package routes

import (
	"net/http"
	"net/url"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/ministryofjustice/modernisation-platform-slackbot/utils"
	"go.uber.org/zap"

	ginzap "github.com/gin-contrib/zap"
)

func parseRepoOwnerAndName(repositoryURL string) (string, string) {
	repoURL := strings.TrimSpace(repositoryURL)
	repoURL = strings.TrimSuffix(repoURL, ".git")

	if parsed, err := url.Parse(repoURL); err == nil {
		path := strings.Trim(parsed.Path, "/")
		parts := strings.Split(path, "/")
		if len(parts) >= 2 && parts[0] != "" && parts[1] != "" {
			return parts[0], parts[1]
		}
	}

	return "ministryofjustice", "cloud-platform-environments"
}

func InitRouter(r *gin.Engine, gh utils.GitHub) {
	owner, repository := parseRepoOwnerAndName(gh.URL)
	InitGetCheckPR(r, gh.Client, owner, repository)
	InitGetRetriggerChecks(r, gh)

	r.GET("/healthz", func(c *gin.Context) {
		c.Status(http.StatusOK)
	})
}

func InitLogger(r *gin.Engine) {
	logger, _ := zap.NewProduction()
	// Add a ginzap middleware, which:
	//   - Logs all requests, like a combined access and error log.
	//   - Logs to stdout.
	//   - RFC3339 with UTC time format.
	r.Use(ginzap.Ginzap(logger, time.RFC3339, true))

	// Logs all panic to error log
	//   - stack means whether output the stack info.
	r.Use(ginzap.RecoveryWithZap(logger, true))
}
