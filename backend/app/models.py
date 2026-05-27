from sqlalchemy import Column, DateTime, Integer, String, Text, func

from .database import Base


class ListingMaster(Base):
    __tablename__ = "listing_master"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    business_name = Column(String(255), nullable=False, index=True)
    category = Column(String(120), nullable=False, index=True)
    city = Column(String(120), nullable=False, index=True)
    address = Column(Text, nullable=False)
    phone = Column(String(40), nullable=True)
    source = Column(String(80), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
