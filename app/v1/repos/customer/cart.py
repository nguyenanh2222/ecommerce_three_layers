from typing import List, Dict
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.associations import CartItemReq


class CartRepository:

    def get_cart(self, customer_id: int) -> Row:
        session: Session = SessionLocal()
        query = f"""
        SELECT * 
        FROM ecommerce.cart c
        WHERE c.customer_id = {customer_id}"""
        rs = session.execute(query).fetchone()
        return rs

    def get_cart_items(self, cart_id: int) -> List[Row]:
        session: Session = SessionLocal()
        query = f"""SELECT cart_items_id, product_id, product_name, quantity, price
        FROM ecommerce.cart_items c
        WHERE cart_id = {cart_id}"""
        rs = session.execute(query).fetchall()
        return rs

    def add_item_to_cart_items(self,
                               customer_id: int,
                               item: CartItemReq) -> List[Row]:
        session: Session = SessionLocal()
        # require: table cart has customer_id -> table customer_id has, c
        query = f"""INSERT INTO cart_items 
        (product_name, 
        quantity, 
        total_price, 
        price, 
        product_id) 
        VALUES (
        '{item.product_name}', 
        {item.quantity}, 
        {item.quantity * item.price},
        {item.price}, 
        {item.product_id} )
        WHERE customer_id = {customer_id}
        RETURNING *"""
        rs = session.execute(query).fetchone()
        session.commit()
        return rs

    def change_item_in_cart_items(self,
                                  product_id: int,
                                  item: CartItemReq) -> Row:
        session: Session = SessionLocal()
        query = f""" UPDATE cart_items
        SET (product_name = '{item.product_name}',
        quantity =  {item.quantity},
        total_price = {item.quantity * item.price},
        price = {item.price},
        product_id {item.product_id} )
        WHERE customer_id = {product_id}
        RETURNING *"""
        rs = session.execute(query).fetchone()
        return rs

    def delete_item_in_cart_items(self,
                                  customer_id: int,
                                  product_id: int) -> List[Row]:
        session: Session = SessionLocal()
        query = f"""
        DELETE FROM cart_items 
        WHERE customer_id = {customer_id} 
        AND product_id = {product_id}
        RETURNING *"""
        rs = session.execute(query).fetchall()
        return rs
