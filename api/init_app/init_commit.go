package init_app

import (
	"github.com/go-git/go-git/v5"
	"github.com/ministryofjustice/cloud-platform-hammer-bot/commit"
)

func InitCommit(url string) (*git.Repository, error) {
	repo, err := commit.OpenRepo()
	if err == nil {
		return repo, nil
	}

	return commit.CloneRepo(url)
}
