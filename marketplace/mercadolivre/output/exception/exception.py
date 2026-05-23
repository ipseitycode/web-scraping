from shared.exception.base_exception import BaseApiException

class OutputException(BaseApiException):
    def __init__(self, code: str, message: str):
        super().__init__(code=code, message=message, stage="output", domain="marketplace", target="mercadolivre")
