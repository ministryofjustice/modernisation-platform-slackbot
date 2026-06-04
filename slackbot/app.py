import json
import logging
import os
import re
import threading
from urllib.parse import urlparse
from typing import Any

import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


NANO_SECOND = 1_000_000_000

def normalize_api_url(raw_url: str) -> str:
    api_url = raw_url.strip().rstrip("/")
    if "://" in api_url:
        return api_url

    # Local/container hosts usually run HTTP only; public hosts should default to HTTPS.
    host = api_url.split("/", 1)[0].split(":", 1)[0].lower()
    local_hosts = {"localhost", "127.0.0.1", "0.0.0.0", "api", "host.docker.internal"}
    scheme = "http" if host in local_hosts else "https"
    return f"{scheme}://{api_url}"

CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")
RAW_API_URL = os.getenv("API_URL", "http://host.docker.internal:3001")
API_URL = normalize_api_url(RAW_API_URL)
GITHUB_URL = os.environ["GITHUB_URL"]
REPOSITORY_URL = re.sub(r"\.git$", "", GITHUB_URL.rstrip("/"))
PARSED_REPOSITORY_URL = urlparse(REPOSITORY_URL)
REPOSITORY_PATH = PARSED_REPOSITORY_URL.path.strip("/")
PULL_URL_PATTERN = re.compile(
    rf"{re.escape(PARSED_REPOSITORY_URL.netloc)}/{re.escape(REPOSITORY_PATH)}/pull/"
)
PULL_ID_PATTERN = re.compile(r"/pull/(\d+)")

CHECKS_CONFIG_PATH = os.getenv(
    "CHECKS_CONFIG_PATH",
    os.path.join(os.path.dirname(__file__), "checks_config.json"),
)

with open(CHECKS_CONFIG_PATH, "r", encoding="utf-8") as config_file:
    CHECKS_CONFIG = json.load(config_file)

CHECKS_CONFIG_PATH = os.getenv(
    "CHECKS_CONFIG_PATH",
    os.path.join(os.path.dirname(__file__), "checks_config.json"),
)

with open(CHECKS_CONFIG_PATH, "r", encoding="utf-8") as config_file:
    CHECKS_CONFIG = json.load(config_file)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if API_URL != RAW_API_URL.strip().rstrip("/"):
    logger.warning("API_URL missing scheme; using normalized URL: %s", API_URL)
else:
    logger.debug("Using API_URL: %s", API_URL)

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)


def get_configured_checks(all_checks: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    categorized: dict[str, list[dict[str, Any]]] = {}
    for check in all_checks:
        name = check.get("Name", "")
        for category, config in CHECKS_CONFIG.items():
            patterns = config.get("name_patterns", [])
            if any(re.search(pattern, name, re.IGNORECASE) is not None for pattern in patterns):
                categorized.setdefault(category, []).append(check)
    return categorized


def get_status_label(status: int) -> str:
    if status == 1:
        return "failed"
    if status == 2:
        return "incomplete"
    return "passed"


def build_checks_summary(data: list[dict[str, Any]]) -> str:
    if not data:
        return "All configured workflow checks have passed."

    lines: list[str] = ["Configured workflow checks:"]

    for pr in data:
        pr_id = pr.get("Id") or pr.get("ID") or "unknown"
        branch = pr.get("Branch", "")

        header = f"- PR #{pr_id}"
        if branch:
            header += f" ({branch})"
        lines.append(header)

        all_checks = pr.get("InvalidChecks") or []
        categorized = get_configured_checks(all_checks)
        configured_checks = [
            check
            for checks in categorized.values()
            for check in checks
        ]

        if not configured_checks:
            lines.append("  - No configured checks with issues or pending status.")
            continue

        for check in configured_checks:
            name = check.get("Name", "Unknown check")
            status_label = get_status_label(int(check.get("Status", 0)))
            url = check.get("URL", "")
            label = f"<{url}|{name}>" if url else name
            lines.append(f"  - {label}: {status_label}")

    return "\n".join(lines)


def get_status(ids: str) -> list[dict[str, Any]]:
    response = requests.get(f"{API_URL}/check-pr", params={"id": ids}, timeout=30)
    response.raise_for_status()
    return response.json()


def remove_emoji(emoji: str, ts: str) -> None:
    app.client.reactions_remove(name=emoji, channel=CHANNEL_ID, timestamp=ts)


def add_emoji(emoji: str, ts: str) -> None:
    app.client.reactions_add(name=emoji, channel=CHANNEL_ID, timestamp=ts)


def post_reply(message: str, ts: str) -> None:
    app.client.chat_postMessage(
        channel=CHANNEL_ID,
        text=message,
        icon_emoji="robot_face",
        thread_ts=ts,
    )


def post_success(data: list[dict[str, Any]], ts: str) -> bool:
    if not data:
        add_emoji("sparkles", ts)
        return True
    return False


def post_fail(data: list[dict[str, Any]], ts: str) -> bool:
    logger.debug("debug fail data some error %s", data)

    all_checks = [check for pr in data for check in pr.get("InvalidChecks", [])]

    configured_checks = get_configured_checks(all_checks)

    has_failure = any(
        check.get("Status") == 1
        for checks in configured_checks.values()
        for check in checks
    )

    if has_failure:
        add_emoji("x", ts)
        post_reply(build_checks_summary(data), ts)
        return True

    return False


def post_reaction(data: list[dict[str, Any]], ts: str) -> bool:
    if post_success(data, ts):
        return True

    if post_fail(data, ts):
        return True

    return False


def retry_later(ids: str, ts: str, retry_in_ms: float) -> None:
    def _retry() -> None:
        data = get_status(ids)
        result = post_reaction(data, ts)
        remove_emoji("repeat", ts)

        if result:
            return

        post_reply(
            "It looks like checks on your pr are _still_ pending even after waiting a while. A Modernisation Platform team member will come and take a look.",
            ts,
        )
        add_emoji("hourglass_flowing_sand", ts)
        add_emoji("warning", ts)

    timer = threading.Timer(retry_in_ms / 1000.0, _retry)
    timer.daemon = True
    timer.start()


def post_pending_recent(data: list[dict[str, Any]], ts: str, ids: str) -> bool:
    pending_recent = [
        pr
        for pr in data
        if pr.get("InvalidChecks")
        and any(
            check.get("Status") == 2 and check.get("RetryInNanoSec", 0) > 0
            for check in pr["InvalidChecks"]
        )
    ]

    if pending_recent:
        retry_in = min(
            check.get("RetryInNanoSec", 0)
            for pr in pending_recent
            for check in pr.get("InvalidChecks", [])
        )

        add_emoji("repeat", ts)
        post_reply(build_checks_summary(data), ts)
        retry_later(ids, ts, (retry_in / NANO_SECOND) * 1000 + 10)
        return True

    return False


@app.event({"type": "message", "subtype": "message_changed"})
def handle_message_changed_events(body: dict[str, Any], logger: logging.Logger) -> None:
    logger.debug("Ignoring message_changed event: %s", body)


@app.event({"type": "message", "subtype": "message_deleted"})
def handle_message_deleted_events(body: dict[str, Any], logger: logging.Logger) -> None:
    logger.debug("Ignoring message_deleted event: %s", body)


@app.message(PULL_URL_PATTERN)
def handle_pull_request_message(message: dict[str, Any], logger: logging.Logger) -> None:
    logger.debug("msg %s", message)

    text = message.get("text", "")
    pull_ids = PULL_ID_PATTERN.findall(text)
    if not pull_ids:
        return

    ids = ",".join(pull_ids)
    data = get_status(ids)

    logger.debug("%s", data)

    message_ts = message["ts"]

    if post_reaction(data, message_ts):
        return

    if post_pending_recent(data, message_ts, ids):
        return

    all_checks = [check for pr in data for check in pr.get("InvalidChecks", [])]

    categorized_checks = get_configured_checks(all_checks)
    configured_checks = [
        check
        for checks in categorized_checks.values()
        for check in checks
    ]

    pending_configured_workflows_paused_older_than_10_mins = any(
        check.get("Status") == 2
        and check.get("RetryInNanoSec", 0) == 0
        and re.search(r"queued", check.get("Message", ""), re.IGNORECASE)
        is not None
        for check in configured_checks
    )

    if pending_configured_workflows_paused_older_than_10_mins:
        add_emoji("hourglass_flowing_sand", message_ts)
        post_reply(
            "One or more configured workflow checks have been queued for over 10 minutes. Please check for any older incomplete workflow runs that may still be blocking these checks.\n\n"
            + build_checks_summary(data),
            message_ts,
        )
        return

    has_pending_configured = any(
        check.get("Status") == 2 for check in configured_checks
    )

    if has_pending_configured:
        add_emoji("hourglass_flowing_sand", message_ts)
        post_reply(
            "Configured workflow checks are still running. I will update this thread once they complete.\n\n"
            + build_checks_summary(data),
            message_ts,
        )


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()