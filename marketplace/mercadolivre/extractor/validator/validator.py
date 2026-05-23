from marketplace.mercadolivre.extractor.exception.exception import ExtractorException

class Validator:
    def validateExtraction(self, data: list):
        if not data:
            raise ExtractorException("EXTRACTOR_SELECTOR_NOT_FOUND", "No fields could be extracted. Selectors might be broken.")
