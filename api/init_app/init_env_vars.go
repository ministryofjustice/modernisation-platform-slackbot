package init_app

import (
	"log"
	"os"
)

func InitEnvVars() (string, string, string, string) {
	githubTokenVal, githubTokenPresent := os.LookupEnv("GITHUB_TOKEN")
	if githubTokenVal == "" || !githubTokenPresent {
		log.Fatal("GITHUB_TOKEN is not set")
	}

	ginMode := "debug"
	ginModeVal, ginModePresent := os.LookupEnv("GIN_MODE")
	if ginModeVal == "" || !ginModePresent {
		if err := os.Setenv("GIN_MODE", ginMode); err != nil {
			log.Fatalf("failed to set GIN_MODE: %v", err)
		}
		ginModeVal = ginMode
	}

	githubURLVal, githubURLPresent := os.LookupEnv("GITHUB_URL")
	if githubURLVal == "" || !githubURLPresent {
		log.Fatal("GITHUB_URL is not set")
	}

	githubUserVal, githubUserPresent := os.LookupEnv("GITHUB_USER")
	if githubUserVal == "" || !githubUserPresent {
		log.Fatal("GITHUB_USER is not set")
	}

	return ginModeVal, githubTokenVal, githubURLVal, githubUserVal
}
