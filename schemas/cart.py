from typing import List

from pydantic import BaseModel, Field


class CartReq:
    ...


class CartRes(BaseModel):
    items: List[CartReq] = Field([])
    product_id: int = Field(None)
    customer_id: int = Field(None)
