from marketplace.mercadolivre.downloader.exception.exception import DownloaderException

class Validator:
    def validateResponse(self, content_list: list):
        if not content_list:
            raise DownloaderException("DOWNLOADER_EMPTY_RESPONSE", "The response from the target was empty.")
