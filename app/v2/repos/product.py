import math
from decimal import Decimal
from typing import List

from sqlalchemy import update, delete, select
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.database import SessionLocal
from models.product import Products
from project.core.schemas import Sort, PageResponse
from schemas.product import ProductReq


class ProductRepository:
    def get_products_repo(
            self, page: int, size: int, product_id: int,
            category: str, product_name: str,
            from_price: Decimal, to_price: Decimal,
            sort_direction: Sort.Direction) -> List[Row]:
        session = SessionLocal()
        stmt = select(Products)
        if product_name:
            stmt = stmt.where(Products.name.like(f"%{product_name}%"))
        if category:
            stmt = stmt.where(Products.category.like(f"%{category}%"))
        if product_id:
            stmt = stmt.where(Products.product_id == product_id)
        if from_price:
            stmt = stmt.where(Products.price >= from_price)
        if to_price:
            stmt = stmt.where(Products.price <= to_price)
        if sort_direction == 'asc':
            stmt = stmt.order_by(Products.created_time)
        if sort_direction == 'desc':
            stmt = stmt.order_by(Products.created_time).desc()
        if page and size is not None:
            stmt.offset((page - 1) * size).limit(size)
        rs = session.execute(stmt).fetchall()
        return rs

    def get_product_by_id_repos(self, product_id: int) -> Row:
        session: Session = SessionLocal()
        stmt = select(Products).where(Products.product_id == product_id)
        rs = session.execute(stmt).fetchone()
        return rs
    #
    # def post_product_repos(self, product: ProductReq, product_id: int) -> Row:
    #     session = SessionLocal()
    #     stmt = session.insert(Products).values(
    #         dict(name=product.name,
    #              description=product.description,
    #              category=product.category,
    #              quantity=product.quantity,
    #              price=product.price,
    #              created_time=product.created_time)).where(
    #         Products.product_id == {product_id}).returning(Products)
    #     rs = session.execute(stmt).fetchone()
    #     session.commit()
    #     return rs
    #
    # def put_product_repos(self, product: ProductReq):
    #     session = SessionLocal()
    #     stmt = update(Products).values(name=product.name,
    #                                    description=product.description,
    #                                    category=product.category,
    #                                    quantity=product.quantity,
    #                                    price=product.price,
    #                                    created_time=product.created_time).returning(Products.product_id)
    #
    #     rs = session.execute(stmt).fetchone()
    #     session.commit()
    #     return rs
    #
    # def delete_product_repos(self, product_id: int) -> Row:
    #     session = SessionLocal()
    #     stmt = (delete(Products).where(Products.product_id == product_id))
    #     rs = session.execute(stmt).fetchone().returning(Products)
    #     session.commit()
    #     return rs

    # def update_product_quantity(self, product_id: int) -> Row:
    #     session = SessionLocal()
    #     stmt = select(Products.quantity - sum(
    #         CartItems.quantity
    #     )).select_from(join(
    #         Products, CartItems, Products.product_id
    #     )).where(
    #         Products.product_id == product_id)
    #     rs = session.execute(stmt).fetchone()
    #     session.commit()
    #     return rs


