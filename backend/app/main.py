import os

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .database import get_db
from .models import ListingMaster
from .schemas import BulkInsertResponse, CountItem, DashboardSummary, ListingCreate, ListingOut

app = FastAPI(title="Business Listings Dashboard API", version="1.0.0")

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/listings/bulk", response_model=BulkInsertResponse, status_code=201)
def bulk_insert_listings(listings: list[ListingCreate], db: Session = Depends(get_db)):
    rows = [ListingMaster(**listing.model_dump()) for listing in listings]
    db.add_all(rows)
    db.commit()
    return {"inserted": len(rows)}


@app.get("/api/listings", response_model=list[ListingOut])
def get_listings(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    stmt = (
        select(ListingMaster)
        .order_by(ListingMaster.created_at.desc(), ListingMaster.id.desc())
        .limit(min(limit, 200))
        .offset(offset)
    )
    return db.scalars(stmt).all()


def grouped_counts(db: Session, column) -> list[CountItem]:
    stmt = (
        select(column.label("name"), func.count(ListingMaster.id).label("count"))
        .group_by(column)
        .order_by(func.count(ListingMaster.id).desc(), column.asc())
    )
    return [CountItem(name=row.name, count=row.count) for row in db.execute(stmt)]


@app.get("/api/dashboard/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    return DashboardSummary(
        city_wise=grouped_counts(db, ListingMaster.city),
        category_wise=grouped_counts(db, ListingMaster.category),
        source_wise=grouped_counts(db, ListingMaster.source),
    )
