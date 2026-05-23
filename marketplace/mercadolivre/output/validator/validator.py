from marketplace.mercadolivre.output.exception.exception import OutputException
from marketplace.mercadolivre.output.transfer.response_transfer import ResponseTransfer

class Validator:
    def validateOutput(self, transfer: ResponseTransfer):
        if not transfer.getTitle():
            raise OutputException("OUTPUT_MISSING_TITLE", "Title is a required field.")
        if transfer.getPrice() is None:
            raise OutputException("OUTPUT_MISSING_PRICE", "Price is a required field.")
        if not transfer.getCurrency():
            raise OutputException("OUTPUT_MISSING_CURRENCY", "Currency is a required field.")
        if not transfer.getUrl():
            raise OutputException("OUTPUT_MISSING_URL", "Url is a required field.")
