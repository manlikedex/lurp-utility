import re
import requests

CURRENT_VERSION = "1.1"

DEVLOG_URL = "https://manlikedex.itch.io/LURP-cache-clear-utility-tool/devlog/1132373/version-11-update"
DOWNLOAD_URL = "https://manlikedex.itch.io/LURP-cache-clear-utility-tool"


def extract_version_from_text(text):
    """
    Extract a version number like 'Version 1.1' or 'v1.1' from HTML.
    """
    patterns = [
        r"[Vv]ersion\s*([0-9]+\.[0-9]+)",
        r"\bv([0-9]+\.[0-9]+)"
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            return match.group(1)

    return None


def check_for_updates():
    """
    Returns tuple:
        (update_available: bool, latest_version: str or None)
    """
    try:
        response = requests.get(DEVLOG_URL, timeout=5)
        html = response.text

        latest_version = extract_version_from_text(html)

        if latest_version is None:
            print("Could not extract version from devlog; ignoring update check.")
            return False, None

        if latest_version.strip() != CURRENT_VERSION.strip():
            return True, latest_version

        return False, latest_version

    except Exception as e:
        print("Update check failed:", e)
        return False, None
