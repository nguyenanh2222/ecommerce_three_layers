from decimal import Decimal
from typing import List
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.associations import CartItems
from schemas.associations import CartItemReq


class CartRepository:

    def get_cart_repo(self, customer_id: int) -> Row:
        session: Session = SessionLocal()
        query = f"""
        SELECT * 
        FROM ecommerce.cart c
        WHERE c.customer_id = {customer_id}"""
        rs = session.execute(query).fetchone()
        return rs

    def get_cart_items_repo(self, cart_id: int) -> List[Row]:
        session: Session = SessionLocal()
        query = f"""SELECT total_price,
        cart_items_id, 
        product_id, 
        product_name, 
        quantity, 
        price
        FROM ecommerce.cart_items c
        WHERE cart_id = {cart_id}"""
        rs = session.execute(query).fetchall()
        return rs

    def get_cart_item_by_id_repo(self, cart_items_id: int) -> Row:
        session: Session = SessionLocal()
        query = f"""SELECT * FROM cart_items
                    WHERE cart_items_id = {cart_items_id}"""
        rs = session.execute(query)
        return rs

    def insert_item_to_cart_items_repo(self, item: CartItems, cart_id: int, total_price: Decimal) -> Row:
        session: Session = SessionLocal()
        query = f"""INSERT INTO cart_items 
        (cart_id,
        product_name, 
        quantity,  
        price, 
        product_id,
        total_price) 
        VALUES (
        {cart_id},
        '{item.product_name}', 
        {item.quantity}, 
        {item.price}, 
        {item.product_id},
        {total_price})
        RETURNING *"""
        session.commit()
        rs = session.execute(query).fetchone()
        session.commit()
        return rs

    def update_item_in_cart_items_repo(self, item: CartItemReq,
                                       cart_id: int, total_price: Decimal,
                                       cart_items_id: int) -> Row:
        session: Session = SessionLocal()
        query = f""" UPDATE cart_items
        SET 
        cart_id = {cart_id},
        product_name = '{item.product_name}',
        quantity =  {item.quantity},
        total_price = {total_price},
        price = {item.price},
        product_id = {item.product_id} 
        WHERE cart_items_id = {cart_items_id} 
        RETURNING *"""
        rs = session.execute(query).fetchone()
        session.commit()
        return rs

    def delete_items_in_cart_items_repo(self, customer_id: int) -> List[Row]:
        session: Session = SessionLocal()
        query = f"""DELETE FROM cart_items
                    WHERE cart_id=(
                    SELECT cart_id FROM cart
                    WHERE customer_id = {customer_id})
                    RETURNING *"""
        rs = session.execute(query)
        session.commit()
        return rs
    def delete_item_in_cart_items_repo(self, cart_item_id: int) -> Row:
        session: Session = SessionLocal()
        query = f"""DELETE FROM cart_items
                            WHERE cart_items_id = {cart_item_id}
                            RETURNING *"""
        rs = session.execute(query).fetchone()
        session.commit()
        return rs