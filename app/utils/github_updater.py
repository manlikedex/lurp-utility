import re
import requests

def _parse_ver(v: str):
    v = v.strip()
    v = v[1:] if v.lower().startswith("v") else v
    parts = re.findall(r"\d+", v)
    parts = (parts + ["0", "0", "0"])[:3]
    return tuple(int(x) for x in parts)

def check_github_update(owner: str, repo: str, current_version: str, timeout: float = 4.0):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    r = requests.get(url, timeout=timeout, headers={"Accept": "application/vnd.github+json"})
    r.raise_for_status()
    data = r.json()

    latest_tag = data.get("tag_name", "")
    release_url = data.get("html_url", "")

    if not latest_tag or not release_url:
        return (False, "", "")

    has_update = _parse_ver(latest_tag) > _parse_ver(current_version)
    return (has_update, latest_tag, release_url)
