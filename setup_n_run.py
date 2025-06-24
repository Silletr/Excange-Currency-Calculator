import os
import sys
import subprocess
from logger_config import logger

REPO_URL = "https://github.com/Silletr/Excange-Currency-Calculator.git"
REPO_DIR = "Excange-Currency-Calculator"


def run_command(cmd, cwd=None):
    try:
        subprocess.run(cmd, cwd=cwd, shell=True, check=True)
    except subprocess.CalledProcessError:
        logger.error(f"Command failed: {cmd}")
        sys.exit(1)


def main():
    # Clone repo if not exist
    if not os.path.isdir(REPO_DIR):
        logger.info("Cloning repository...")
        run_command(f"git clone {REPO_URL}")

    # Installing the requirements
    logger.info("Installing requirements...")
    pip_cmd = "pip install -r requirements.txt"
    run_command(pip_cmd, cwd=REPO_DIR)

    # starting streamlit
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.local/bin")
    logger.info("Launching Streamlit app...")
    run_command("streamlit run main.py", cwd=REPO_DIR)


if __name__ == "__main__":
    main()
