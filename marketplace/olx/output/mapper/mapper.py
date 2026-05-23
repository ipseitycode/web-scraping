from marketplace.olx.extractor.transfer.request_transfer import RequestTransfer
from marketplace.olx.output.transfer.response_transfer import ResponseTransfer

class Mapper:
    def mapProduct(self, raw_data: RequestTransfer) -> ResponseTransfer:
        transfer = ResponseTransfer()

        transfer.setTitle(raw_data.getTitle())
        transfer.setPrice(raw_data.getPrice())
        transfer.setUrl(raw_data.getUrl())
        transfer.setLocation(raw_data.getLocation())
        transfer.setDate(raw_data.getDate())
        transfer.setImage(raw_data.getImage())
        transfer.setInstallments(raw_data.getInstallments())

        badges = raw_data.getBadges()
        transfer.setBadges(badges if badges else None)

        img_count = raw_data.getImageCount()
        transfer.setImageCount(int(img_count) if img_count is not None else None)

        return transfer
