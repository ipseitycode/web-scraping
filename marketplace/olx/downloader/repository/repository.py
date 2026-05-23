import json
import time
import re
import unicodedata
from pathlib import Path
from marketplace.olx.shared.config.settings import CACHE_ENABLED, CACHE_EXPIRATION_MINUTES

class Repository:
    def __init__(self):
        self.__cache_dir = Path(__file__).parent.parent.parent / "shared" / "infra" / "cache"
        if not self.__cache_dir.exists():
            self.__cache_dir.mkdir(parents=True, exist_ok=True)

    def __normalize_query(self, query: str) -> str:
        q = query.lower()
        q = unicodedata.normalize('NFKD', q).encode('ASCII', 'ignore').decode('utf-8')
        q = re.sub(r'[^a-z0-9]+', '-', q)
        return q.strip('-')

    def __build_cache_key(self, estado: str, query: str) -> str:
        norm_query = self.__normalize_query(query)
        st = estado if estado else "brasil"
        return f"olx_{st}_{norm_query}.json"

    def findCache(self, estado: str, query: str):
        if not CACHE_ENABLED:
            return None

        key = self.__build_cache_key(estado, query)
        file_path = self.__cache_dir / key

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            timestamp = data.get("_timestamp")
            if not timestamp:
                return None

            age_minutes = (time.time() - timestamp) / 60
            if age_minutes > CACHE_EXPIRATION_MINUTES:
                return None

            return data.get("results")
        except Exception:
            return None

    def saveCache(self, estado: str, query: str, data: list):
        if not CACHE_ENABLED:
            return

        key = self.__build_cache_key(estado, query)
        file_path = self.__cache_dir / key

        payload = {
            "_timestamp": time.time(),
            "results": data
        }

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False)
        except Exception:
            pass
