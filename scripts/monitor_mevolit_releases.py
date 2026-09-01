#!/usr/bin/env python3
"""Detect the current iOS beta from Mevolit's upstream data feed and ingest it."""

import base64
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MEVOLIT_BETA_FEED_URL = "https://api.github.com/repos/macadmins/sofa/contents/data/resources/apple_beta_feed.json"
MEVOLIT_STABLE_FEED_URL = "https://api.github.com/repos/macadmins/sofa/contents/data/resources/bulletin_data.json"
SUPPORTED_PLATFORMS = ("macOS", "iOS", "iPadOS", "tvOS", "watchOS", "visionOS", "Xcode")
STABLE_PLATFORM_NAMES = {"ios": "iOS", "ipados": "iPadOS", "macos": "macOS", "safari": "Safari", "tvos": "tvOS", "visionos": "visionOS", "watchos": "watchOS"}


def fetch_json(url, description, headers=None):
  request_headers = {"User-Agent": "Mevolit-release-monitor/1.0", "Accept": "application/vnd.github+json"}
  request_headers.update(headers or {})
  request = Request(url, headers=request_headers)
  try:
    with urlopen(request, timeout=30) as response:
      return json.loads(response.read().decode("utf-8"))
  except HTTPError as error:
    raise ValueError(f"{description} returned HTTP {error.code}") from error


def fetch_feed(url, description):
  response = fetch_json(url, description)
  if response.get("encoding") != "base64" or not response.get("content"):
    raise ValueError(f"{description} returned an unexpected GitHub response")
  return json.loads(base64.b64decode(response["content"]).decode("utf-8"))


def fetch_releases():
  feed = fetch_feed(MEVOLIT_BETA_FEED_URL, "Mevolit beta feed")
  latest_betas = {}
  for item in feed.get("items", []):
    platform = item.get("platform")
    if platform in SUPPORTED_PLATFORMS and item.get("version") and item.get("build"):
      release = {
        "platform": platform,
        "channel": "Developer Beta",
        "version": item["version"],
        "build": item["build"],
        "notesUrl": item.get("release_notes_url", ""),
      }
      if platform not in latest_betas or item.get("released", "") > latest_betas[platform]["released"]:
        latest_betas[platform] = {"released": item.get("released", ""), "release": release}
  releases = [item["release"] for item in latest_betas.values()]
  stable_feed = fetch_feed(MEVOLIT_STABLE_FEED_URL, "Mevolit stable release feed")
  for platform_key, item in stable_feed.get("latest_releases", {}).items():
    platform = STABLE_PLATFORM_NAMES.get(platform_key)
    if platform and item.get("version") and item.get("build"):
      releases.append({
        "platform": platform,
        "channel": "Public Release",
        "version": item["version"],
        "build": item["build"],
        "notesUrl": item.get("url", ""),
      })
  if not releases:
    raise ValueError("Could not find supported releases in the Mevolit data feeds")
  return releases


def ingest_release(portal_url, api_token, release):
  payload = json.dumps({
    "platform": release["platform"],
    "channel": release["channel"],
    "version": release["version"],
    "build": release["build"],
    "notesUrl": release["notesUrl"],
  }).encode("utf-8")
  request = Request(
    f"{portal_url.rstrip('/')}/api/release-ingest",
    data=payload,
    method="POST",
    headers={
      "Authorization": f"Bearer {api_token}",
      "Content-Type": "application/json",
      "Accept": "application/json",
      "User-Agent": "Mozilla/5.0 (compatible; MevolitReleaseMonitor/1.0)",
    },
  )
  try:
    with urlopen(request, timeout=30) as response:
      return json.loads(response.read().decode("utf-8"))
  except HTTPError as error:
    raise ValueError(f"Admin portal release-ingest endpoint returned HTTP {error.code}") from error


def main():
  portal_url = os.environ.get("ADMIN_PORTAL_URL", "")
  api_token = os.environ.get("ADMIN_API_TOKEN", "")
  if not portal_url or not api_token:
    raise ValueError("ADMIN_PORTAL_URL and ADMIN_API_TOKEN must be configured")
  results = []
  for release in fetch_releases():
    result = ingest_release(portal_url, api_token, release)
    results.append({**release, **result})
  print(json.dumps(results))


if __name__ == "__main__":
  try:
    main()
  except (HTTPError, URLError, ValueError) as error:
    print(f"Release monitor failed: {error}", file=sys.stderr)
    sys.exit(1)