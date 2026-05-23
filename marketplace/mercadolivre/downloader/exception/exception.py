from shared.exception.base_exception import BaseApiException

class DownloaderException(BaseApiException):
    def __init__(self, code: str, message: str):
        super().__init__(code=code, message=message, stage="downloader", domain="marketplace", target="mercadolivre")
