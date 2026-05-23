from shared.exception.base_exception import BaseApiException

class OutputException(BaseApiException):
    pass

def raiseOutputMissingTitle(domain: str, target: str):
    raise OutputException(
        code="OUTPUT_MISSING_TITLE",
        message="Item sem title após o mapeamento.",
        stage="output",
        domain=domain,
        target=target
    )

def raiseOutputMissingPrice(domain: str, target: str):
    raise OutputException(
        code="OUTPUT_MISSING_PRICE",
        message="Item sem price após o mapeamento.",
        stage="output",
        domain=domain,
        target=target
    )

def raiseOutputMissingUrl(domain: str, target: str):
    raise OutputException(
        code="OUTPUT_MISSING_URL",
        message="Item sem url após o mapeamento.",
        stage="output",
        domain=domain,
        target=target
    )
