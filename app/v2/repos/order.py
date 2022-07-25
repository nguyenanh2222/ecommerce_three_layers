import math
from datetime import datetime
from typing import List, Dict
from sqlalchemy import select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.order import Orders
from order_status import EOrderStatus
from project.core.schemas import Sort, PageResponse


class OrderRepository:

    def get_order_repo(self,
                       page: int,
                       size: int,
                       customer_name: str,
                       order_id: int,
                       product_name: str,
                       sort_direction: Sort.Direction,
                       ) -> Dict:
        session : Session = SessionLocal()
        stmt = select(Orders)
        if order_id:
            stmt = stmt.where(Orders.order_id == order_id)
        if customer_name:
            stmt = stmt.where(Orders.customer_name.like(f"%{customer_name}%"))
        if product_name:
            stmt = stmt.where(Orders.customer_name.like(f"%{product_name}%"))
        if sort_direction == 'asc':
            stmt = stmt.order_by(Orders.created_time)
        if sort_direction == 'desc':
            stmt = stmt.order_by(Orders.created_time).desc()
        rs = session.execute(stmt).fetchall()
        total_page = math.ceil(len(rs) / size)
        total_items = len(rs)
        if page and size is not None:
            stmt.offset((page - 1) * size).limit(size)
        current_page = page
        result = {'data': rs,
                  'total_page': total_page,
                  'total_items': total_items,
                  'current_page': current_page}
        return result

    def change_status_repos(self, order_id: int,
                            next_status: EOrderStatus) -> Row:
        session: Session = SessionLocal()
        stmt = update(Orders).values(
            Orders.status == f'{next_status}'
        ).where(
            Orders.order_id == {order_id}).returning(Orders)
        session.commit()
        rs = session.execute(stmt).fetchone()
        session.commit()
        return rs

    # def insert_order(self, customer_id: int, cart_id: int):
    #
    #     query = f""" INSERT INTO ecommerce.orders (
    #         total_amount, customer_id,status, time_open)
    #         SELECT SUM(total_price),
    #         {customer_id},
    #         'OPEN',
    #         '{datetime.now()}'
    #         FROM cart_items
    #         WHERE cart_id = {cart_id} RETURNING *"""
    #     session = SessionLocal()
    #     session.select(Orders).where(Orders.order_id == )
    #
    #     session.commit()
    #     return rs
    #
    # def insert_order_item(self, order_id: int) -> Row:
    #     query = f"""
    #             INSERT INTO order_items
    #             (product_id,
    #             product_name,
    #             quantity,
    #             price,
    #             total_price,
    #             order_id)
    #             SELECT product_id,
    #             product_name,
    #             quantity,
    #             price,
    #             total_price,
    #             {order_id}
    #             FROM cart_items c
    #             RETURNING *"""
    #
    #     session: Session = SessionLocal()
    #     rs = session.execute(query).fetchall()
    #     return rs
    #
    #
    #
    # def delete_item_in_cart_items_repo(self, customer_id: int) -> Row:
    #     session: Session = SessionLocal()
    #     query = f"""
    #         DELETE FROM cart_items ci
    #         JOIN cart c
    #         ON ci.cart_id = c.cart_id
    #         WHERE cart_items_id = {customer_id}
    #         RETURNING *"""
    #     rs = session.execute(query).fetchone()
    #     session.commit()
    #     return rs
