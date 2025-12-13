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
    bat_path = exe_path + ".update.bat"

    # Download new exe
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    # Write updater batch file
    with open(bat_path, "w") as f:
        f.write(f"""@echo off
echo Updating application...
ping 127.0.0.1 -n 3 > nul
move /y "{tmp_path}" "{exe_path}"
start "" "{exe_path}"
del "%~f0"
""")

    # Run updater
    subprocess.Popen(
        ["cmd.exe", "/c", bat_path],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    # Exit app so EXE unlocks
    sys.exit(0)

