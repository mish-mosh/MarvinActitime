import os

from dotenv import load_dotenv

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
ENV_FILE = os.path.join(PROJECT_DIR, ".env")

if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

MARVIN_SYNC_SERVER = os.environ.get("MARVIN_SYNC_SERVER", "")
MARVIN_SYNC_DATABASE = os.environ.get("MARVIN_SYNC_DATABASE", "")
MARVIN_SYNC_USER = os.environ.get("MARVIN_SYNC_USER", "")
MARVIN_SYNC_PASSWORD = os.environ.get("MARVIN_SYNC_PASSWORD", "")
MARVIN_CONNECTION_STRING = (
    f"https://{MARVIN_SYNC_USER}:{MARVIN_SYNC_PASSWORD}@{MARVIN_SYNC_SERVER}"
)


ACTITIME_BASE_URI = os.environ.get("ACTITIME_BASE_URI", "")
ACTITIME_USERNAME = os.environ.get("ACTITIME_USERNAME", "")
ACTITIME_USER_ID = os.environ.get("ACTITIME_USER_ID", "")
ACTITIME_CREDENTIALS = os.environ.get("ACTITIME_CREDENTIALS", "")

PINNED_TASKS_YAML_PATH = os.environ.get(
    "PINNED_TASKS_YAML_PATH", f"{PROJECT_DIR}/pinned_tasks.yaml"
)

OVERTIME_FOLDER_PATH = os.environ.get("OVERTIME_FOLDER_PATH", "")
CSV_DELIMITER = ","
