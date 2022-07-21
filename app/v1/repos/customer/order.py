from typing import List
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.database import SessionLocal
from order_status import EOrderStatus
from project.core.schemas import Sort
from schemas.order import OrderReq


class OrderRepository:
    def get_order_repo(self,
                       page: int,
                       size: int,
                       customer_name: str,
                       order_id: int,
                       product_name: str,
                       sort_direction: Sort.Direction,
                       ) -> List[Row]:
        query = f"""
    SELECT oi.order_id, oi.product_name, o.customer_id
    FROM ecommerce.orders o
    JOIN ecommerce.order_items oi 
    ON o.order_id = oi.order_id"""
        parameters = [order_id, product_name, customer_name]
        for parameter in parameters:
            if parameter:
                query += " WHERE "
                break
        if order_id:
            query += f" o.order_id = {order_id} AND"
        if customer_name:
            query += f" o.customer_id = {customer_name} AND"
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

    #place_order
    def insert_order(self,
                    customer_id: int,
                    order: OrderReq) -> int:
        session = SessionLocal()
        # insert into orders
        query = f""" INSERT INTO ecommerce.orders (customer_id)
        VALUES ({customer_id}) RETURNING *"""
        _rs = session.execute(query)
        order_id = _rs.fetchone()['order_id']
        return order_id

    # def insert_order_item(self, customer_id: int):
        # insert items into order_items
        # -> value -> product_id, product_name, quantity, price, total_price
        # from cart

        # subtraction product quantity

    # def select_product_quantity(self):
    #     ...
        # query = f"""SELECT ci.product_id, SUM(ci.quantity)
        #             FROM cart_items ci
        #             JOIN cart c
        #             ON c.cart_id  = ci.cart_id
        #             WHERE customer_id = {customer_id}
        #             GROUP BY ci.product_id
        #             """
        # _rs: CursorResult = session.execute(query)
        # quans_cart = _rs.fetchall()
        # for item in quans_cart:
        #     query = f""" SELECT p.product_id, p.quantity
        #     FROM ecommerce.products p
        #     JOIN ecommerce.order_items oi2
        #     ON oi2.product_id = p.product_id
        #     WHERE p.product_id = {item[0]}
        # """
        #     _rs = session.execute(query)
        # quans_product = _rs.fetchall()

        # update product
    # def update_product_quantity(self):
        # for item_c in quans_cart:
        #     for item_p in quans_product:
        #         if item_p[0] == item_c[0]:
        #             sub_product = item_p[1] - item_c[1]
        #             if sub_product < 0:
        #                 ...
        #             query = f""" UPDATE products
        #             SET  quantity = {sub_product}
        #             WHERE product_id = {item_p[0]}"""
        #             _rs = session.execute(query)

 # delete item in cart_items -> ham co viet trong cart roi
 #    def delete_item_in_cart_items_repo(self, cart_items_id: int) -> Row:
 #        session: Session = SessionLocal()
 #        query = f"""
 #            DELETE FROM cart_items
 #            WHERE cart_items_id = {cart_items_id}
 #            RETURNING *"""
 #        rs = session.execute(query).fetchone()
 #        session.commit()
 #        return rs
