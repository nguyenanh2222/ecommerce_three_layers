from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class Permission(BaseModel):
    user_name: str = Field()
    password: str = Field()


