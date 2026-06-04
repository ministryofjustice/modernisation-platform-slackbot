#!/bin/sh

set -eu

: "${SLACK_BOT_TOKEN:?SLACK_BOT_TOKEN must be set}"
: "${SLACK_SIGNING_SECRET:?SLACK_SIGNING_SECRET must be set}"
: "${SLACK_APP_TOKEN:?SLACK_APP_TOKEN must be set}"
: "${GITHUB_URL:?GITHUB_URL must be set}"

docker run --rm \
  -e SLACK_BOT_TOKEN="$SLACK_BOT_TOKEN" \
  -e SLACK_SIGNING_SECRET="$SLACK_SIGNING_SECRET" \
  -e SLACK_APP_TOKEN="$SLACK_APP_TOKEN" \
  -e GITHUB_URL="$GITHUB_URL" \
  -e API_URL="${API_URL:-http://host.docker.internal:3001}" \
  slackbot-local