from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    user_type: str


class UserShow(BaseModel):
    username: str
    user_type: str


class InvoiceCreate(BaseModel):
    customer_name: str
    unit_prices: str
    rent: float





class InvoiceOut(BaseModel):
    id: int
    customer_name: str
    total_quantity: int
    total_amount: float
    date: datetime
    unit_prices: str
    rent: float
 # The printable invoice text

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
