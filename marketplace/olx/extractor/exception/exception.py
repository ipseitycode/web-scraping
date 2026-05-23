from shared.exception.base_exception import BaseApiException

class ExtractorException(BaseApiException):
    pass

def raiseExtractorSelectorNotFound(domain: str, target: str):
    raise ExtractorException(
        code="EXTRACTOR_SELECTOR_NOT_FOUND",
        message="Nenhum card encontrado — seletores possivelmente quebrados pela mudança do HTML do site.",
        stage="extractor",
        domain=domain,
        target=target
    )
