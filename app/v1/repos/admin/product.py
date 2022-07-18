from decimal import Decimal
from typing import List
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.database import SessionLocal
from project.core.schemas import Sort
from schemas.product import ProductReq


class ProductRepository:
    def get_products_repo(
            self, page: int, size: int, product_id: int,
            category: str, product_name: str,
            from_price: Decimal, to_price: Decimal, sort_direction: Sort.Direction) -> List:
        query = f""" SELECT * FROM ecommerce.orders o
        JOIN ecommerce.order_items oi 
        ON o.order_id = oi.order_id"""
        parameters = [category, product_name, product_id,
                      from_price, to_price, sort_direction]
        for parameter in parameters:
            if parameter:
                query += " WHERE "
                break
        if product_id:
            query += f" product_id = {product_id} AND"
        if category:
            query += f" category LIKE '%{category}%' AND"
        if product_name:
            query += f" product_name LIKE '%{product_name}%' AND"
        if from_price:
            query += f" price >= {from_price} AND"
        if to_price:
            query += f" price <= {to_price} AND"
        if query.endswith("AND"):
            query = query[:-3]
        if sort_direction:
            query += f" ORDER BY time_open {sort_direction}"
        session: Session = SessionLocal()
        query += f" LIMIT {size} OFFSET {(page - 1) * size}"
        _rs = session.execute(query)
        _rs = _rs.fetchall()
        return _rs

    def get_product_by_id_repos(self, product_id: int) -> Row:
        session: Session = SessionLocal()
        query = f'SELECT * FROM products WHERE product_id = {product_id}'
        _rs = session.execute(query).fetchone()
        return _rs

    def put_product_repos(self, product: ProductReq, product_id: int) -> Row:
        session: Session = SessionLocal()
        query = f"""UPDATE products SET description = '{product.description}',\
        name = '{product.name}', quantity = '{product.quantity}',
        created_time = '{product.created_time}' 
        WHERE product_id = {product_id} RETURNING *"""
        _rs = session.execute(query).fetchone()
        session.commit()
        return _rs

    def delete_product_repos(self, product_id: int) -> Row:
        session: Session = SessionLocal()
        query = f"DELETE FROM products WHERE product_id = {product_id} RETUNING *"
        _rs = session.execute(query)
        session.commit()
        return _rs
