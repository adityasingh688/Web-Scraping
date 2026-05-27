from datetime import datetime

from pydantic import BaseModel, Field


class ListingCreate(BaseModel):
    business_name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=120)
    city: str = Field(..., min_length=1, max_length=120)
    address: str = Field(..., min_length=1)
    phone: str | None = Field(default=None, max_length=40)
    source: str = Field(..., min_length=1, max_length=80)


class ListingOut(ListingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CountItem(BaseModel):
    name: str
    count: int


class DashboardSummary(BaseModel):
    city_wise: list[CountItem]
    category_wise: list[CountItem]
    source_wise: list[CountItem]


class BulkInsertResponse(BaseModel):
    inserted: int
