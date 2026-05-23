from shared.exception.base_exception import BaseApiException

class ExtractorException(BaseApiException):
    def __init__(self, code: str, message: str):
        super().__init__(code=code, message=message, stage="extractor", domain="marketplace", target="mercadolivre")
