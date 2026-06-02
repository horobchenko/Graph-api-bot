import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DOWNLOADS_DIR = DATA_DIR / "downloads"
CHROMA_DIR = DATA_DIR / "chroma"

DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TELEGRAM_ADMIN_IDS = [int(x.strip()) for x in os.getenv("TELEGRAM_ADMIN_IDS", "").split(",") if x.strip()]
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "")
SHAREPOINT_SITE_ID = os.getenv("SHAREPOINT_SITE_ID", "")
