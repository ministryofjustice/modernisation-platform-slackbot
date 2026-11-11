package main

import (
	"log"
	"net"
	"net/http"

	"github.com/ministryofjustice/modernisation-platform-slackbot/init_app"
	"github.com/ministryofjustice/modernisation-platform-slackbot/utils"
)

func main() {
	ginMode, ghToken, ghURL, ghUser := init_app.InitEnvVars()

	ghClient, ghErr := init_app.InitGH(ghToken)
	if ghErr != nil {
		log.Fatal("Error initialising github client: ", ghErr)
	}

	ghRepo, ghErr := init_app.InitCommit(ghURL)
	if ghErr != nil {
		log.Fatal("Error initialising github repo: ", ghErr)
	}

	gh := utils.GitHub{Token: ghToken, URL: ghURL, User: ghUser, Repo: ghRepo, Client: ghClient}

	r := init_app.InitGin(ginMode, gh)
	addr := ":3000"

	log.Printf("Starting HTTP server on %s", addr)

	listener, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatal("Error binding server port: ", err)
	}

	log.Printf("HTTP server listening on %s (port bind complete)", addr)

	err = http.Serve(listener, r)
	if err != nil {
		log.Fatal("Error starting server: ", err)
	}
}
