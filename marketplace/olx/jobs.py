from marketplace.olx.shared.infra.cache.cleaner import clean_expired_cache

def register_jobs(scheduler):
    scheduler.add_job(clean_expired_cache, "cron", hour=3)
