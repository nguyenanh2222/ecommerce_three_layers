from typing import List
from pydantic import BaseModel, Field

from models.associations import CartItems


class CartReq:
    ...



class CartRes(BaseModel):
    cart_items: List = Field([])
    product_id: int = Field(None)
    customer_id: int = Field(None)



