#!/usr/bin/env python3
"""Publish the vuln-triage-launch-100 campaign via linkedctl.

Modelled on publish-agentic-senior-leverage-100.py. Stops immediately on an
API failure or an unparseable response so an ambiguous result can never
create duplicates on retry.

The manifest is rewritten atomically after every single post, so an
interrupted run resumes exactly where it stopped: already-published posts
are no longer "ready" and are skipped.

Usage:
  python3 scripts/publish-vuln-triage-launch-100.py [--limit N] [--dry-run]

--limit publishes at most N of the remaining ready posts, so the campaign
can be released in batches rather than all at once.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "docs/linkedin-publish/vuln-triage-launch-100"
INDEX = CAMPAIGN / "index.json"
LOG = CAMPAIGN / "publication-log.jsonl"


def atomic_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def record(event: dict) -> None:
    with LOG.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event) + "\n")
    print(json.dumps(event), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="max posts to publish (0 = all)")
    parser.add_argument("--dry-run", action="store_true", help="print the plan, publish nothing")
    args = parser.parse_args()

    manifest = json.loads(INDEX.read_text(encoding="utf-8"))
    posts = manifest["posts"]
    ready = [post for post in posts if post["status"] == "ready"]
    if args.limit > 0:
        ready = ready[: args.limit]

    if not ready:
        print("No ready posts remain.")
        return 0

    if args.dry_run:
        print(f"Would publish {len(ready)} post(s):")
        for post in ready:
            print(f"  post-{post['number']:03d}  [{post['track']}]  {post['title']}")
        return 0

    environment = dict(os.environ)
    environment["LINKEDCTL_API_VERSION"] = "202601"

    for post in ready:
        number = post["number"]
        path = CAMPAIGN / f"post-{number:03d}.txt"
        command = [
            "npx", "-y", "linkedctl", "post", "create",
            "--visibility", "PUBLIC", "--text-file", str(path), "--format", "json",
        ]
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            timeout=90,
        )
        timestamp = datetime.now(timezone.utc).isoformat()

        if result.returncode != 0:
            record(
                {
                    "number": number,
                    "status": "failed",
                    "at": timestamp,
                    "returnCode": result.returncode,
                    "stderr": result.stderr.strip(),
                }
            )
            return result.returncode or 1

        try:
            urn = json.loads(result.stdout)["urn"]
        except (json.JSONDecodeError, KeyError) as error:
            record(
                {
                    "number": number,
                    "status": "ambiguous-response",
                    "at": timestamp,
                    "stdout": result.stdout.strip(),
                    "error": str(error),
                }
            )
            return 2

        post["status"] = "published"
        post["publication"] = {"urn": urn, "publishedAt": timestamp}
        manifest["status"] = (
            "published" if all(p["status"] == "published" for p in posts) else "publishing"
        )
        atomic_json(INDEX, manifest)
        record({"number": number, "status": "published", "at": timestamp, "urn": urn})

    return 0


if __name__ == "__main__":
    sys.exit(main())
