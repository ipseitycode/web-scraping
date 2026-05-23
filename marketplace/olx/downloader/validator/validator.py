from marketplace.olx.downloader.exception.exception import raiseDownloaderEmptyResponse

class Validator:
    def validateResponse(self, raw_contents: list, domain: str, target: str):
        if not raw_contents:
            raiseDownloaderEmptyResponse(domain, target)
