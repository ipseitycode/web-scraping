from marketplace.olx.output.exception.exception import (
    raiseOutputMissingTitle,
    raiseOutputMissingPrice,
    raiseOutputMissingUrl
)
from marketplace.olx.output.transfer.response_transfer import ResponseTransfer

class Validator:
    def validateOutput(self, transfer: ResponseTransfer, domain: str, target: str):
        if not transfer.getTitle():
            raiseOutputMissingTitle(domain, target)
        if not transfer.getPrice():
            raiseOutputMissingPrice(domain, target)
        if not transfer.getUrl():
            raiseOutputMissingUrl(domain, target)
