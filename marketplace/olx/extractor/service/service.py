from bs4 import BeautifulSoup
from shared.base.base_extractor import BaseExtractor
from marketplace.olx.extractor.transfer.request_transfer import RequestTransfer
from marketplace.olx.extractor.validator.validator import Validator

class Service(BaseExtractor):
    def __init__(self):
        self.__validator = Validator()

    def _extract(self, raw_contents: list) -> list:
        extracted_data = []

        for html in raw_contents:
            soup = BeautifulSoup(html, "html.parser")
            cards = soup.select('section.olx-adcard')

            for card in cards:
                transfer = RequestTransfer()

                title_el = card.select_one('h2.olx-adcard__title')
                if title_el:
                    transfer.setTitle(title_el.get_text(strip=True))

                price_el = card.select_one('h3.olx-adcard__price')
                if price_el:
                    transfer.setPrice(price_el.get_text(strip=True))

                url_el = card.select_one('a[data-testid="adcard-link"]')
                if url_el:
                    transfer.setUrl(url_el.get('href'))

                loc_el = card.select_one('p.olx-adcard__location')
                if loc_el:
                    transfer.setLocation(loc_el.get_text(strip=True))

                date_el = card.select_one('p.olx-adcard__date')
                if date_el:
                    transfer.setDate(date_el.get_text(strip=True))

                img_el = card.select_one('.olx-adcard__media img')
                if img_el:
                    transfer.setImage(img_el.get('src'))

                inst_el = card.select_one('[data-testid="adcard-price-info"]')
                if inst_el:
                    transfer.setInstallments(inst_el.get_text(strip=True))

                badges_els = card.select('.olx-adcard__badges div')
                if badges_els:
                    badges = [b.get_text(strip=True) for b in badges_els]
                    transfer.setBadges(badges)

                img_count_els = card.select('.olx-adcard__carousel--bullet')
                if img_count_els:
                    transfer.setImageCount(len(img_count_els))

                extracted_data.append(transfer)

        self.__validator.validateExtraction(extracted_data, "marketplace", "olx")

        return extracted_data
