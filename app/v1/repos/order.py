import math
from datetime import datetime
from typing import List, Dict
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.database import SessionLocal
from order_status import EOrderStatus
from project.core.schemas import Sort


class OrderRepository:

    def get_order_repo(self,
                       page: int,
                       size: int,
                       customer_name: str,
                       order_id: int,
                       product_name: str,
                       sort_direction: Sort.Direction,
                       ) -> Dict:
        query = f"""
    SELECT o.order_id, oi.product_name, o.customer_id
    FROM ecommerce.orders o
    JOIN ecommerce.order_items oi 
    ON o.order_id = oi.order_id
    JOIN ecommerce.customers c
    ON o.customer_id = c.customer_id
    """
        parameters = [order_id, product_name, customer_name]
        for parameter in parameters:
            if parameter:
                query += " WHERE "
                break
        if order_id:
            query += f" o.order_id = {order_id} AND"
        if customer_name:
            query += f" c.name = '{customer_name}' AND"
        if product_name:
            query += f" product_name LIKE '%{product_name}%' AND"
        if query.endswith("AND"):
            query = query[:-3]
        if sort_direction:
            query += f" ORDER BY time_open {sort_direction}"
        session: Session = SessionLocal()
        rs = session.execute(query).fetchall()
        total_page = math.ceil(len(rs) / size)
        total_items = len(rs)
        query += f" LIMIT {size} OFFSET {(page - 1) * size}"
        rs = session.execute(query).fetchall()
        current_page = page
        result = {'data': rs,
                  'total_page': total_page,
                  'total_items': total_items,
                  'current_page': current_page}
        return result

    def change_status_repos(self,
                            order_id: int,
                            next_status: EOrderStatus) -> Row:
        session: Session = SessionLocal()
        query = f""" UPDATE ecommerce.orders 
        SET status = '{next_status}' 
        WHERE order_id = {order_id} 
        RETURNING *"""
        rs = session.execute(query).fetchone()
        session.commit()
        return rs

    def insert_order(self, customer_id: int, cart_id: int):
        query = f""" INSERT INTO ecommerce.orders (
            total_amount, customer_id,status, time_open) 
            SELECT SUM(total_price),
            {customer_id},
            'OPEN', 
            '{datetime.now()}'
            FROM cart_items
            WHERE cart_id = {cart_id} RETURNING *"""
        session = SessionLocal()
        rs = session.execute(query).fetchone()
        session.commit()
        return rs

    def insert_order_item(self, order_id: int) -> Row:
        query = f"""         
                INSERT INTO order_items
                (product_id, 
                product_name, 
                quantity, 
                price, 
                total_price, 
                order_id)
                SELECT product_id, 
                product_name,
                quantity, 
                price, 
                total_price,
                {order_id}
                FROM cart_items c
                RETURNING *"""

        session: Session = SessionLocal()
        rs = session.execute(query).fetchall()
        return rs

    def delete_item_in_cart_items_repo(self, customer_id: int) -> Row:
        session: Session = SessionLocal()
        query = f"""
            DELETE FROM cart_items ci
            JOIN cart c
            ON ci.cart_id = c.cart_id
            WHERE cart_items_id = {customer_id}
            RETURNING *"""
        rs = session.execute(query).fetchone()
        session.commit()
        return rs
