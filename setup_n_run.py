import os
import sys
import subprocess
import platform

REPO_URL = "https://github.com/Silletr/Excange-Currency-Calculator.git"
REPO_DIR = "Excange-Currency-Calculator"


def run_command(cmd, cwd=None):
    try:
        subprocess.run(cmd, cwd=cwd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"[ERROR] Command failed: {cmd}")
        sys.exit(1)


def main():
    # Set the Operational system
    system = platform.system()
    print(f"[INFO] Detected OS: {system}")

    # Clone repo if not exist
    if not os.path.isdir(REPO_DIR):
        print("[INFO] Cloning repository...")
        run_command(f"git clone {REPO_URL}")

    # Installing the requirements
    print("[INFO] Installing requirements...")
    pip_cmd = "pip install -r requirements.txt"
    run_command(pip_cmd, cwd=REPO_DIR)

    # starting streamlit
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.local/bin")
    path_to_st = os.environ["PATH"]
    print("[INFO] Launching Streamlit app...")
    run_command(f"{path_to_st}", cwd=REPO_DIR)


if __name__ == "__main__":
    main()
