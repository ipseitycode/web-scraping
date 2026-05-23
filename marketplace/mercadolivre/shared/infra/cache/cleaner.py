import json
from datetime import datetime, timedelta
from pathlib import Path

_CACHE_DIR = Path(__file__).parent
_MAX_AGE_HOURS = 48



def clean_expired_cache():
    cutoff = datetime.now() - timedelta(hours=_MAX_AGE_HOURS)

    for file in _CACHE_DIR.glob("*.json"):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[cache-cleaner] removing unreadable file {file.name}: {e}")
            file.unlink(missing_ok=True)
            continue

        raw_ts = data.get("_timestamp")
        if not raw_ts:
            print(f"[cache-cleaner] removing file without timestamp: {file.name}")
            file.unlink(missing_ok=True)
            continue

        try:
            ts = datetime.fromisoformat(raw_ts)
        except ValueError as e:
            print(f"[cache-cleaner] removing file with invalid timestamp {file.name}: {e}")
            file.unlink(missing_ok=True)
            continue

        if ts < cutoff:
            file.unlink(missing_ok=True)
            print(f"[cache-cleaner] removed expired {file.name}")
