import requests
import sys
import subprocess

OWNER = "Schwandt-Dev"
REPO = "Deck_Coach"
APP_NAME = "Deck_Coach.exe"
CURRENT_VERSION = "1.0.0"


def check_for_updates():
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return

    data = response.json()
    latest_version = data["tag_name"].lstrip("v")

    if latest_version == CURRENT_VERSION:
        return

    choice = input(
        f"Update available ({CURRENT_VERSION} → {latest_version}). Update now? (y/n): "
    ).lower()

    if choice != "y":
        return

    for asset in data["assets"]:
        if asset["name"] == APP_NAME:
            download_update(asset["browser_download_url"])
            return


def download_update(url):
    exe_path = sys.executable
    tmp_path = exe_path + ".new"

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    # Replace exe safely using a restart trick
    subprocess.Popen(
        [
            "cmd",
            "/c",
            "timeout /t 1 > nul && "
            f"move /y \"{tmp_path}\" \"{exe_path}\" && "
            f"start \"\" \"{exe_path}\""
        ],
        shell=True
    )

    sys.exit()

