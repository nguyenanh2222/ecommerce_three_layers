from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProductReq(BaseModel):
    name: str = Field(...)
    quantity: int = Field(...)
    price: Decimal = Field(...)
    description: str = Field(...)
    category: str = Field(...)
    created_time: datetime = Field(...)


class ProductRes(BaseModel):
    product_id: int = Field(None)
    name: str = Field(None)
    quantity: int = Field(None)
    price: float = Field(None)
    description: str = Field(None)
    category: str = Field(None)
    created_time: datetime = Field(None)
