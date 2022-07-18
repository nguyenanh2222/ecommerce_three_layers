from pydantic import BaseModel, Field


class CustomerReq(BaseModel):
    name: str = Field(...)
    phone: str = Field(...)
    address: str = Field(...)
    email: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)


class CustomerRes(BaseModel):
    customer_id: int = Field(None)
    password: str = Field(None)
    name: str = Field(None)
    phone: str = Field(None)
    address: str = Field(None)
    email: str = Field(None)
    username: str = Field(None)


class CustomerUpdate(BaseModel):
    name: str = Field(None)
    phone: str = Field(None)
    address: str = Field(None)
    email: str = Field(None)