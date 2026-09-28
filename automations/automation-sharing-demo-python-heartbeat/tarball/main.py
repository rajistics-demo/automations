"""Small, LLM-free cron job for the Rajistics automation sharing demo."""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone


def fire_callback(status="COMPLETED", error=None):
    """Signal run completion. MUST be called on every exit path — success AND error."""
    url = os.environ.get("AUTOMATION_CALLBACK_URL", "")
    if not url: return
    body = {"status": status, "run_id": os.environ.get("AUTOMATION_RUN_ID", "")}
    if error: body["error"] = error
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=json.dumps(body).encode(), headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('AUTOMATION_CALLBACK_API_KEY', '')}",
        }))
    except Exception as e: print(f"Callback error: {e}")


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"Rajistics shared automation demo ran at {timestamp}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        fire_callback("FAILED", str(exc))
        print(f"Automation failed: {exc}", file=sys.stderr)
        raise
    else:
        fire_callback("COMPLETED")
