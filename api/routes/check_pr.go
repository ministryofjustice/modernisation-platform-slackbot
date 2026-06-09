package routes

import (
	"net/http"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/google/go-github/v57/github"
	"github.com/ministryofjustice/cloud-platform-hammer-bot/pull_requests"
	"github.com/ministryofjustice/cloud-platform-hammer-bot/utils"
)

type PrChecks struct {
	ID            string `json:"Id"`
	Branch        string `json:"Branch"`
	InvalidChecks []pull_requests.InvalidChecks
}

func InitGetCheckPR(r *gin.Engine, ghClient *github.Client, owner, repository string) {
	r.GET("/check-pr", func(c *gin.Context) {
		ids := c.Query("id")
		splitIds := strings.Split(ids, ",")

		var allPRStatuses []PrChecks

		for _, id := range splitIds {
			checks, resp, ghErr := ghClient.Checks.ListCheckRunsForRef(c, owner, repository, "refs/pull/"+id+"/head", &github.ListCheckRunsOptions{Filter: github.String("all")})

			if ghErr != nil {
				obj := utils.Response{
					Status: resp.StatusCode,
					Error:  []string{ghErr.Error()},
				}
				utils.SendResponse(c, obj)
				return
			}
			data := pull_requests.CheckPRStatus(checks, time.Since)

			if len(data) == 0 {
				continue
			}

			branch, err := pull_requests.GetBranch(ghClient, owner, repository, id)
			if err != nil {
				obj := utils.Response{
					Status: http.StatusInternalServerError,
					Error:  []string{err.Error()},
				}
				utils.SendResponse(c, obj)
				return
			}

			allPRStatuses = append(allPRStatuses, PrChecks{
				id,
				branch,
				data,
			})
		}

		obj := utils.Response{
			Status: http.StatusOK,
			Data:   allPRStatuses,
		}
		utils.SendResponse(c, obj)
	})
}
