from decimal import Decimal

from pydantic import BaseModel, Field


class CartItemReq(BaseModel):
    price: float = Field(...)
    quantity: int = Field(...)
    total_price: int = Field(...)
    product_id: int = Field(...)
    product_name: str = Field(...)


class CartItemsRes(BaseModel):
    product_id: int = Field(None)
    customer_id: int = Field(None)


class OrderItemsReq(BaseModel):
    customer_name: str = Field(...)
    product_name: str = Field(...)
    quantity: int = Field(...)
    price: Decimal = Field(...)
    total_price: Decimal = Field(...)


class OrderItemsRes(BaseModel):
    product_id: int = Field(None)
    order_id: int = Field(None)
    customer_name: str = Field(None)
    product_name: str = Field(None)
    quantity: int = Field(None)
    price: Decimal = Field(None)
    total_price: Decimal = Field(None)