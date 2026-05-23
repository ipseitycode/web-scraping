from marketplace.olx.extractor.exception.exception import raiseExtractorSelectorNotFound

class Validator:
    def validateExtraction(self, data: list, domain: str, target: str):
        if not data:
            raiseExtractorSelectorNotFound(domain, target)
