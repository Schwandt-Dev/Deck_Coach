import requests
import sys
import subprocess
import os
import time


OWNER = "Schwandt-Dev"
REPO = "Deck_Coach"
APP_NAME = "Deck_Coach.exe"



def check_for_updates(CURRENT_VERSION, HARM_MESSAGE):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return

    data = response.json()
    latest_version = data["tag_name"].lstrip("v")

    if latest_version == CURRENT_VERSION:
        return

    print(f"Update available ({CURRENT_VERSION} → {latest_version}). Update now? (y/n): ")
    if HARM_MESSAGE != '': print(HARM_MESSAGE)
    choice = input().lower()

    if choice != "y":
        return

    for asset in data["assets"]:
        if asset["name"] == APP_NAME:
            download_update(asset["browser_download_url"])
    create_update_bat()
    subprocess.Popen([os.path.join(os.getcwd(), "update.bat")], creationflags=subprocess.CREATE_NEW_CONSOLE)
    sys.exit(0)     
        


def download_update(url):
    # Determine target folder
    target_folder = os.path.join(os.getcwd(), "Deck_Coach")
    os.makedirs(target_folder, exist_ok=True)
    time.sleep(5)
    # Paths for temporary download
    exe_path = os.path.join(target_folder, APP_NAME)         # where the final exe will live
                                 # temporary download

    # Download new EXE to .new file
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(exe_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

    print(f"New version downloaded to: {exe_path}")

def create_update_bat():
    target_folder = os.getcwd()
    exe_name = "Deck_Coach.exe"
    old_exe = os.path.join(target_folder, exe_name)
    new_exe = os.path.join(target_folder, exe_name)  # same name as downloaded
    bat_path = os.path.join(target_folder, "update.bat")

    with open(bat_path, "w") as f:
        f.write(f"""@echo off
echo Applying update...
rem Wait a few seconds to allow current EXE to exit
timeout /t 3 /nobreak >nul

:wait
tasklist /FI "IMAGENAME eq {exe_name}" 2>NUL | find /I "{exe_name}" >NUL
if not errorlevel 1 (
    echo Waiting for current application to exit...
    timeout /t 2 /nobreak >nul
    goto wait
)

rem Remove old EXE if it exists
if exist "{old_exe}" del /f "{old_exe}"

rem Rename new EXE to proper name (overwrite)
ren "{new_exe}" "{exe_name}"

echo Update applied successfully!
del "%~f0"
""")