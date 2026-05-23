from typing import Optional, List, Literal, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel, Field

from marketplace.olx.downloader.transfer.request_transfer import RequestTransfer
from marketplace.olx.downloader.service.service import Service as DownloaderService
from marketplace.olx.downloader.repository.repository import Repository
from marketplace.olx.extractor.service.service import Service as ExtractorService
from marketplace.olx.output.service.service import Service as OutputService

router = APIRouter()

AllowedField = Literal[
    "title", "price", "url", "location", "date", 
    "image", "installments", "badges", "image_count"
]

class FiltersSchema(BaseModel):
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    has_installments: Optional[bool] = None
    location: Optional[str] = None

    class Config:
        extra = "forbid"

class SearchPayload(BaseModel):
    query: str
    estado: Optional[str] = "brasil"
    filters: Optional[FiltersSchema] = None
    fields: Optional[List[AllowedField]] = None
    limit: Optional[int] = Field(None, gt=0)

    class Config:
        extra = "forbid"

@router.post("/marketplace/olx")
def search_olx(payload: SearchPayload):
    req_transfer = RequestTransfer()
    req_transfer.setQuery(payload.query)
    req_transfer.setEstado(payload.estado)
    req_transfer.setDomain("marketplace")
    req_transfer.setTarget("olx")
    
    filters_dict = payload.filters.dict(exclude_none=True) if payload.filters else {}
    req_transfer.setFilters(filters_dict)

    repository = Repository()
    
    cached_data = repository.findCache(payload.estado, payload.query)
    
    if cached_data is not None:
        final_results = OutputService.applyFiltersAndProjection(
            cached_data, 
            filters_dict, 
            payload.limit, 
            payload.fields
        )
        return {
            "success": True,
            "domain": "marketplace",
            "target": "olx",
            "query": payload.query,
            "total": len(final_results),
            "cached": True,
            "results": final_results
        }

    downloader = DownloaderService()
    raw_contents = downloader.executeDownload(req_transfer)
    
    extractor = ExtractorService()
    extracted_data = extractor.executeExtraction(raw_contents)
    
    output = OutputService()
    processed_data = output.executeOutput(extracted_data)
    
    complete_results = [item.toJson() for item in processed_data]
    
    repository.saveCache(payload.estado, payload.query, complete_results)
    
    final_results = OutputService.applyFiltersAndProjection(
        complete_results, 
        filters_dict, 
        payload.limit, 
        payload.fields
    )
    
    return {
        "success": True,
        "domain": "marketplace",
        "target": "olx",
        "query": payload.query,
        "total": len(final_results),
        "cached": False,
        "results": final_results
    }
