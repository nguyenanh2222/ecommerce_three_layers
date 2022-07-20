from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, validator
from starlette import status


class ProductReq(BaseModel):
    name: str = Field(max_length=60, default="AZ111")
    quantity: int = Field(gt=0, default=1)
    price: Decimal = Field(gt=0, default=50_000)
    description: str = Field(max_length=500, default="Summer Clothes")
    category: str = Field(max_length=50, default="A")
    created_time: datetime = Field(default_factory=datetime.now)


class ProductRes(BaseModel):
    product_id: int = Field(None)
    name: str = Field(None, max_length=50)
    quantity: int = Field(None, gt=0)
    price: Decimal = Field(gt=0, default_factory=50_000)
    description: str = Field(None, max_length=500)
    category: str = Field(None, max_length=50)
    created_time: datetime = Field(None)

    @validator('created_time', pre=True, always=True)
    def set_created_time_now(cls, v):
        return v or datetime.now()

