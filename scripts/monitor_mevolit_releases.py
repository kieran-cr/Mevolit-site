#!/usr/bin/env python3
"""Detect the current iOS beta from Mevolit's upstream data feed and ingest it."""

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MEVOLIT_BETA_FEED_URL = "https://raw.githubusercontent.com/macadmins/sofa/main/data/resources/apple_beta_feed.json"


def fetch_text(url):
  request = Request(url, headers={"User-Agent": "Mevolit-release-monitor/1.0"})
  with urlopen(request, timeout=30) as response:
    return response.read().decode("utf-8", errors="replace")


def fetch_ios_release():
  feed = json.loads(fetch_text(MEVOLIT_BETA_FEED_URL))
  for item in feed.get("items", []):
    if item.get("platform") == "iOS" and item.get("version") and item.get("build"):
      return item["version"], item["build"], item.get("release_notes_url", "")
  raise ValueError("Could not find an iOS beta version and build in the Mevolit data feed")


def ingest_release(portal_url, api_token, version, build, notes_url):
  payload = json.dumps({
    "platform": "iOS",
    "channel": "Developer Beta",
    "version": version,
    "build": build,
    "notesUrl": notes_url,
  }).encode("utf-8")
  request = Request(
    f"{portal_url.rstrip('/')}/api/release-ingest",
    data=payload,
    method="POST",
    headers={"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"},
  )
  with urlopen(request, timeout=30) as response:
    return json.loads(response.read().decode("utf-8"))


def main():
  portal_url = os.environ.get("ADMIN_PORTAL_URL", "")
  api_token = os.environ.get("ADMIN_API_TOKEN", "")
  if not portal_url or not api_token:
    raise ValueError("ADMIN_PORTAL_URL and ADMIN_API_TOKEN must be configured")
  version, build, notes_url = fetch_ios_release()
  result = ingest_release(portal_url, api_token, version, build, notes_url)
  print(json.dumps({"version": version, "build": build, **result}))


if __name__ == "__main__":
  try:
    main()
  except (HTTPError, URLError, ValueError) as error:
    print(f"Release monitor failed: {error}", file=sys.stderr)
    sys.exit(1)