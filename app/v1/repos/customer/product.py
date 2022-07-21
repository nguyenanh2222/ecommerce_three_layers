from decimal import Decimal
from typing import List
from sqlalchemy.engine import Row, CursorResult
from sqlalchemy.orm import Session
from db.database import SessionLocal
from project.core.schemas import Sort
from schemas.product import ProductReq


# class ProductRepositoryCus:
    # def get_product