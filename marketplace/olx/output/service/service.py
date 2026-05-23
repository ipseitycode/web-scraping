import logging
from shared.base.base_output import BaseOutput
from marketplace.olx.output.mapper.mapper import Mapper
from marketplace.olx.output.validator.validator import Validator
from marketplace.olx.output.exception.exception import OutputException

class Service(BaseOutput):
    def __init__(self):
        self.__mapper = Mapper()
        self.__validator = Validator()

    def _process(self, raw_data_list: list) -> list:
        processed_data = []

        for raw_item in raw_data_list:
            transfer = self.__mapper.mapProduct(raw_item)

            try:
                self.__validator.validateOutput(transfer, "marketplace", "olx")
                processed_data.append(transfer)
            except OutputException as e:
                logging.warning(f"Item descartado: {str(e)}")
                continue

        return processed_data

    @staticmethod
    def applyFiltersAndProjection(results: list, filters: dict, limit: int, fields: list) -> list:
        filtered = []
        for item in results:
            keep = True
            if filters:
                if 'price_min' in filters or 'price_max' in filters:
                    price_str = item.get("price")
                    if not price_str:
                        keep = False
                    else:
                        try:
                            clean_price = price_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
                            price_float = float(clean_price)
                            if 'price_min' in filters and price_float < filters['price_min']:
                                keep = False
                            if 'price_max' in filters and price_float > filters['price_max']:
                                keep = False
                        except ValueError:
                            keep = False

                if 'has_installments' in filters and filters['has_installments']:
                    if not item.get("installments"):
                        keep = False

                if 'location' in filters and filters['location']:
                    loc = item.get("location")
                    if not loc or filters['location'].lower() not in loc.lower():
                        keep = False

            if keep:
                filtered.append(item)

        if limit is not None:
            filtered = filtered[:limit]

        if fields is not None:
            projected = []
            for item in filtered:
                proj = {k: v for k, v in item.items() if k in fields}
                projected.append(proj)
            return projected

        return filtered
