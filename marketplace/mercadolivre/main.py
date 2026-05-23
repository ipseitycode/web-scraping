from typing import Literal
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from marketplace.mercadolivre.downloader.transfer.request_transfer import RequestTransfer
from marketplace.mercadolivre.downloader.repository.repository import Repository
from marketplace.mercadolivre.downloader.configuration.configuration import Configuration
from marketplace.mercadolivre.downloader.service.service import Service as DownloaderService
from marketplace.mercadolivre.extractor.service.service import Service as ExtractorService
from marketplace.mercadolivre.output.service.service import Service as OutputService, applyFiltersAndFields


AllowedField = Literal[
    "title", "price", "currency", "url",
    "rating", "price_original", "installments", "shipping", "seller",
]


class FiltersPayload(BaseModel):
    model_config = ConfigDict(extra='forbid')
    price_min: float | None = None
    price_max: float | None = None
    free_shipping: bool | None = None
    min_rating: float | None = None
    has_discount: bool | None = None
    seller: str | None = None


class SearchPayload(BaseModel):
    query: str
    filters: FiltersPayload = FiltersPayload()
    fields: list[AllowedField] | None = None
    limit: int | None = Field(default=None, gt=0)


router = APIRouter()


@router.post("/marketplace/mercadolivre")
def scrape_mercadolivre(payload: SearchPayload):
    filters_dict = payload.filters.model_dump(exclude_none=True)
    fields = payload.fields
    limit = payload.limit
    max_items = Configuration().setupMaxItems()

    request_transfer = RequestTransfer()
    request_transfer.setQuery(payload.query)
    request_transfer.setDomain("marketplace")
    request_transfer.setTarget("mercadolivre")
    request_transfer.setFilters(filters_dict)

    repository = Repository()
    normalized_query = "-".join(payload.query.strip().lower().split())
    cache_key = f"mercadolivre_{normalized_query}"
    cached_result = repository.findCache(cache_key)

    if cached_result:
        capped = cached_result[:max_items]
        shaped = applyFiltersAndFields(capped, filters_dict, fields, limit)
        return {
            "success": True,
            "domain": "marketplace",
            "target": "mercadolivre",
            "query": payload.query,
            "total": len(shaped),
            "cached": True,
            "results": shaped
        }

    downloader = DownloaderService()
    raw_content = downloader.executeDownload(request_transfer)

    extractor = ExtractorService()
    extracted_data = extractor.executeExtraction(raw_content)

    output = OutputService()
    processed_data = output.executeOutput(extracted_data)

    full_results = [item.toJson() for item in processed_data][:max_items]
    repository.saveCache(cache_key, full_results)

    shaped = applyFiltersAndFields(full_results, filters_dict, fields, limit)

    return {
        "success": True,
        "domain": "marketplace",
        "target": "mercadolivre",
        "query": payload.query,
        "total": len(shaped),
        "cached": False,
        "results": shaped
    }
