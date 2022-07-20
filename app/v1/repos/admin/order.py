from typing import List

from fastapi import Depends
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from app.v1.router.admin.permission import get_user
from app.v1.service.admin.order import OrderService
from db.database import SessionLocal
from order_status import EOrderStatus
from project.core.schemas import Sort


class OrderRepository:
    def get_order_repo(self, page: int,
                       size: int, order_id: int,
                       product_name: str,
                       customer_name: str,
                       sort_direction: Sort.Direction,
                       service: OrderService = Depends(get_user)) -> List[Row]:
        query = f"""
    SELECT * 
    FROM ecommerce.orders o
    JOIN ecommerce.order_items oi 
    ON o.order_id = oi.order_id
    JOIN ecommerce.customers c
    ON c.customer_id = o.customer_id"""
        parameters = [order_id, product_name, customer_name]
        for parameter in parameters:
            if parameter:
                query += " WHERE "
                break
        if order_id:
            query += f" o.order_id = {order_id} AND"
        if customer_name:
            query += f" c.name LIKE '%{customer_name}%' AND"
        if product_name:
            query += f" product_name LIKE '%{product_name}%' AND"
        if query.endswith("AND"):
            query = query[:-3]
        if sort_direction:
            query += f" ORDER BY time_open {sort_direction}"
        session: Session = SessionLocal()
        query += f" LIMIT {size} OFFSET {(page - 1) * size}"
        rs = session.execute(query).fetchall()
        return rs

    def change_order_repo(self, order_id: int,
                          next_status: EOrderStatus,
                          service: OrderService = Depends(get_user)) -> Row:
        session: Session = SessionLocal()
        query = f""" UPDATE ecommerce.orders 
        SET status = '{next_status}' 
        WHERE order_id = {order_id} 
        RETURNING *"""
        rs = session.execute(query).fetchone()
        session.commit()
        return rs


