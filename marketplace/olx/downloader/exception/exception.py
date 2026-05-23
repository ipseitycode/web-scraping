from shared.exception.base_exception import BaseApiException

class DownloaderException(BaseApiException):
    pass

def raiseDownloaderEmptyResponse(domain: str, target: str):
    raise DownloaderException(
        code="DOWNLOADER_EMPTY_RESPONSE",
        message="Nenhuma página coletada (timeout em todas as tentativas).",
        stage="downloader",
        domain=domain,
        target=target
    )
