import os
import json
from datetime import datetime, timedelta
from marketplace.mercadolivre.shared.config import settings as module_settings

class Repository:
    def __init__(self):
        self.__cache_dir = os.path.join(os.path.dirname(__file__), "..", "..", "shared", "infra", "cache")
        os.makedirs(self.__cache_dir, exist_ok=True)

    def __getFilePath(self, key: str) -> str:
        return os.path.join(self.__cache_dir, f"{key}.json")

    def findCache(self, key: str):
        if not module_settings.CACHE_ENABLED:
            return None

        file_path = self.__getFilePath(key)
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            timestamp = datetime.fromisoformat(data["_timestamp"])
            expiration = timestamp + timedelta(minutes=module_settings.CACHE_EXPIRATION_MINUTES)

            if datetime.now() > expiration:
                return None

            return data["response"]
        except Exception:
            return None

    def saveCache(self, key: str, response: dict):
        if not module_settings.CACHE_ENABLED:
            return

        file_path = self.__getFilePath(key)
        data = {
            "_timestamp": datetime.now().isoformat(),
            "response": response
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
