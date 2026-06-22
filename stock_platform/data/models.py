from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class StockInfo(Base):
    __tablename__ = "stock_info"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String)
    sector = Column(String)
    industry = Column(String)
    exchange = Column(String)
    is_active = Column(Boolean, default=True)

    prices = relationship("StockPrice", back_populates="stock")

class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stock_info.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    stock = relationship("StockInfo", back_populates="prices")

    __table_args__ = (UniqueConstraint('stock_id', 'timestamp', name='uix_stock_timestamp'),)
