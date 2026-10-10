import argparse
import json
import subprocess
import sys
from pathlib import Path


ALLOWED_PAYLOAD_FIELDS = frozenset({"body", "comments", "commit_id"})


class PendingReviewError(Exception):
    pass


def repository_name(value):
    owner, separator, name = value.partition("/")
    if not separator or not owner or not name or "/" in name:
        raise argparse.ArgumentTypeError("repository must be owner/repo")
    return value


def pull_request_number(value):
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("pull request must be a positive integer") from error
    if number < 1:
        raise argparse.ArgumentTypeError("pull request must be a positive integer")
    return number


def load_payload(path):
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PendingReviewError(f"cannot read payload: {error}") from error
    if not isinstance(payload, dict):
        raise PendingReviewError("payload must be a JSON object")
    unsupported = sorted(set(payload) - ALLOWED_PAYLOAD_FIELDS)
    if unsupported:
        if "event" in unsupported:
            raise PendingReviewError("payload must not contain event; pending reviews cannot be submitted")
        raise PendingReviewError(f"payload contains unsupported fields: {', '.join(unsupported)}")
    return payload


def gh_json(*arguments):
    try:
        result = subprocess.run(
            ["gh", "api", *arguments],
            capture_output=True,
            check=False,
            text=True,
        )
    except OSError as error:
        raise PendingReviewError(f"cannot run gh api: {error}") from error
    if result.returncode:
        raise PendingReviewError(result.stderr.strip() or "gh api failed")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise PendingReviewError(f"gh api returned invalid JSON: {error}") from error


def reviews(value):
    if not isinstance(value, list):
        raise PendingReviewError("gh api returned an invalid reviews response")
    if all(isinstance(page, list) for page in value):
        return [review for page in value for review in page]
    return value


def post_pending_review(repository, pull_request, payload_path):
    load_payload(payload_path)
    endpoint = f"repos/{repository}/pulls/{pull_request}/reviews"
    existing = reviews(gh_json(endpoint, "--paginate", "--slurp"))
    if any(isinstance(review, dict) and review.get("state") == "PENDING" for review in existing):
        raise PendingReviewError("a pending review already exists; refusing to add to or replace it")
    review = gh_json("-X", "POST", endpoint, "--input", str(payload_path))
    if not isinstance(review, dict) or review.get("state") != "PENDING":
        raise PendingReviewError("GitHub did not create a PENDING review")
    review_id = review.get("id")
    url = review.get("html_url") or review.get("url")
    if review_id is None or not isinstance(url, str) or not url:
        raise PendingReviewError("GitHub did not return the pending review id and URL")
    print(f"Pending review {review_id}: {url}")


def parse_arguments(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=repository_name)
    parser.add_argument("pull_request", type=pull_request_number)
    parser.add_argument("payload", type=Path)
    return parser.parse_args(arguments)


def main(arguments=None):
    args = parse_arguments(arguments)
    try:
        post_pending_review(args.repository, args.pull_request, args.payload)
    except PendingReviewError as error:
        print(f"post_pending_review: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
