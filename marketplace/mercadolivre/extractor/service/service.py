from bs4 import BeautifulSoup
from shared.base.base_extractor import BaseExtractor
from marketplace.mercadolivre.extractor.transfer.request_transfer import RequestTransfer
from marketplace.mercadolivre.extractor.validator.validator import Validator

class Service(BaseExtractor):
    def __init__(self):
        self.__validator = Validator()

    def _extract(self, raw_content_list: list):
        extracted_data = []
        
        for html in raw_content_list:
            soup = BeautifulSoup(html, "html.parser")
            cards = soup.select("li.ui-search-layout__item")
            
            for card in cards:
                transfer = RequestTransfer()
                
                title_elem = card.select_one("a.poly-component__title")
                if title_elem:
                    transfer.setTitle(title_elem.get_text(strip=True))
                    transfer.setUrl(title_elem.get("href"))
                    
                price_elem = card.select_one("span.andes-money-amount__fraction")
                if price_elem:
                    transfer.setPrice(price_elem.get_text(strip=True))
                    
                rating_elem = card.select_one("span.poly-component__review-compacted span.poly-phrase-label")
                if rating_elem:
                    transfer.setRating(rating_elem.get_text(strip=True))
                    
                price_original_elem = card.select_one("s.andes-money-amount--previous span.andes-money-amount__fraction")
                if price_original_elem:
                    transfer.setPriceOriginal(price_original_elem.get_text(strip=True))
                    
                installments_elem = card.select_one("span.poly-price__installments")
                if installments_elem:
                    transfer.setInstallments(installments_elem.get_text(separator=' ', strip=True))
                    
                shipping_elem = card.select_one("div.poly-component__shipping")
                if not shipping_elem:
                    shipping_elem = card.select_one("div.poly-component__shipping-v2")
                if shipping_elem:
                    transfer.setShipping(shipping_elem.get_text(separator=' ', strip=True))
                    
                seller_elem = card.select_one("span.poly-component__seller")
                if seller_elem:
                    seller_text = seller_elem.find(string=True, recursive=False)
                    if seller_text:
                        transfer.setSeller(seller_text.strip())
                        
                extracted_data.append(transfer)
                
        self.__validator.validateExtraction(extracted_data)
        return extracted_data
