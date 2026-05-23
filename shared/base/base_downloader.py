import time
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseDownloader(ABC):

    def __init__(self, retry_attempts: int, delay_seconds: int):
        self.__retry_attempts = retry_attempts
        self.__delay_seconds = delay_seconds

    def executeDownload(self, request):
        query = request.getQuery()
        attempts = 0

        while attempts < self.__retry_attempts:
            attempts += 1
            logger.info(f"[downloader] attempt {attempts}/{self.__retry_attempts} — query: '{query}'")

            try:
                result = self._fetch(request)
                logger.info(f"[downloader] success on attempt {attempts}")
                return result

            except Exception as e:
                logger.warning(f"[downloader] attempt {attempts} failed: {e}")
                if attempts < self.__retry_attempts:
                    logger.info(f"[downloader] waiting {self.__delay_seconds}s before retry")
                    time.sleep(self.__delay_seconds)
                else:
                    logger.error(f"[downloader] all {self.__retry_attempts} attempts exhausted")
                    raise

    @abstractmethod
    def _fetch(self, request):
        pass
