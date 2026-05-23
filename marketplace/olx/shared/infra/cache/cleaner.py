import time
import json
from pathlib import Path

def clean_expired_cache():
    cache_dir = Path(__file__).parent
    
    if not cache_dir.exists():
        return
        
    current_time = time.time()
    max_age_seconds = 48 * 3600
    
    for file_path in cache_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            timestamp = data.get("_timestamp")
            
            if not timestamp or (current_time - timestamp) > max_age_seconds:
                file_path.unlink()
        except Exception:
            try:
                file_path.unlink()
            except Exception:
                pass
