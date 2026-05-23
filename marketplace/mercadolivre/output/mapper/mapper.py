from marketplace.mercadolivre.extractor.transfer.request_transfer import RequestTransfer
from marketplace.mercadolivre.output.transfer.response_transfer import ResponseTransfer

class Mapper:
    def mapProduct(self, raw: RequestTransfer) -> ResponseTransfer:
        response = ResponseTransfer()
        
        response.setTitle(raw.getTitle() if raw.getTitle() else None)
        response.setUrl(raw.getUrl() if raw.getUrl() else None)
        
        try:
            if raw.getPrice():
                price = float(raw.getPrice().replace('.', '').replace(',', '.'))
                response.setPrice(price)
            else:
                response.setPrice(None)
        except ValueError:
            response.setPrice(None)
            
        try:
            if raw.getRating():
                rating = float(raw.getRating().replace(',', '.'))
                response.setRating(rating)
            else:
                response.setRating(None)
        except ValueError:
            response.setRating(None)
            
        try:
            if raw.getPriceOriginal():
                price_original = float(raw.getPriceOriginal().replace('.', '').replace(',', '.'))
                response.setPriceOriginal(price_original)
            else:
                response.setPriceOriginal(None)
        except ValueError:
            response.setPriceOriginal(None)
            
        response.setInstallments(raw.getInstallments() if raw.getInstallments() else None)
        response.setShipping(raw.getShipping() if raw.getShipping() else None)
        response.setSeller(raw.getSeller() if raw.getSeller() else None)
        
        return response
