from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(String(50), nullable=False)


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    total_quantity = Column(Integer, nullable=False)
    total_amount = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    unit_prices = Column(String(255), nullable=False)
    rent = Column(Float, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
