import logging
from shared.base.base_output import BaseOutput
from marketplace.mercadolivre.output.mapper.mapper import Mapper
from marketplace.mercadolivre.output.validator.validator import Validator
from marketplace.mercadolivre.output.exception.exception import OutputException

logger = logging.getLogger(__name__)


def applyFiltersAndFields(items: list, filters: dict = None, fields: list = None, limit: int = None) -> list:
    filters = filters or {}
    filtered = [item for item in items if _passesFilters(item, filters)]
    if limit is not None:
        filtered = filtered[:limit]
    if fields is not None:
        return [{k: item.get(k) for k in fields} for item in filtered]
    return filtered


def _passesFilters(item: dict, filters: dict) -> bool:
    price_min = filters.get("price_min")
    if price_min is not None and (item.get("price") is None or item["price"] < price_min):
        return False

    price_max = filters.get("price_max")
    if price_max is not None and (item.get("price") is None or item["price"] > price_max):
        return False

    if filters.get("free_shipping") is True:
        shipping = item.get("shipping")
        if not shipping or "grátis" not in shipping.lower():
            return False

    min_rating = filters.get("min_rating")
    if min_rating is not None:
        rating = item.get("rating")
        if rating is None or rating < min_rating:
            return False

    if filters.get("has_discount") is True:
        if item.get("price_original") is None:
            return False

    seller_filter = filters.get("seller")
    if seller_filter is not None:
        seller = item.get("seller")
        if not seller or seller_filter.casefold() not in seller.casefold():
            return False

    return True


class Service(BaseOutput):
    def __init__(self):
        self.__mapper = Mapper()
        self.__validator = Validator()

    def _process(self, raw_data_list: list) -> list:
        processed_data = []
        for raw in raw_data_list:
            response_transfer = self.__mapper.mapProduct(raw)
            try:
                self.__validator.validateOutput(response_transfer)
                processed_data.append(response_transfer)
            except OutputException as exc:
                logger.warning(f"[output] item descartado: {exc.code} — {exc}")
        return processed_data
