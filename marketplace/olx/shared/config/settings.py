import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")

CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_EXPIRATION_MINUTES = int(os.getenv("CACHE_EXPIRATION_MINUTES", 1440))
HTTP_TIMEOUT_SECONDS = int(os.getenv("HTTP_TIMEOUT_SECONDS", 30))
HTTP_RETRY_ATTEMPTS = int(os.getenv("HTTP_RETRY_ATTEMPTS", 3))
HTTP_DELAY_SECONDS = int(os.getenv("HTTP_DELAY_SECONDS", 2))