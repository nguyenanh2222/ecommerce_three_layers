from decimal import Decimal
from typing import List

from sqlalchemy import select, insert, update, delete
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.database import SessionLocal
from models.associations import CartItems
from models.cart import Cart
from schemas.associations import CartItemReq


class CartRepository:
    def get_cart_repo(self, customer_id: int) -> Row:
        session: Session = SessionLocal()
        stmt = select(Cart).where(
            Cart.customer_id == customer_id)
        rs = session.execute(stmt).fetchone()
        print(type(rs[0]))
        return rs

    def get_cart_items_repo(self, cart_id: int) -> List[Row]:
        session: Session = SessionLocal()
        stmt = select(Cart, CartItems).where(
            Cart.customer_id == cart_id).join(Cart.cart_id).returning(Cart)
        rs = session.execute(stmt).fetchall()
        return rs

    def insert_item_to_cart_items_repo(
            self, item: CartItems, cart_id: int, total_price: Decimal) -> Row:
        session: Session = SessionLocal()
        stmt = (
            insert(CartItems).values(cart_id=cart_id,
                                     product_name=item.product_name,
                                     quantity=item.quantity,
                                     price=item.price,
                                     product_id=item.product_id,
                                     total_price=total_price)
        ).returning(CartItems)
        rs = session.execute(stmt).fetchone()
        return rs

    def update_item_in_cart_items_repo(self, item: CartItemReq,
                                       cart_id: int, total_price: Decimal,
                                       cart_items_id: int) -> Row:
        session: Session = SessionLocal()
        stmt = (
            update(CartItems).where(
                CartItems.cart_item_id == cart_items_id
            ).values(cart_id=cart_id,
                     product_name=item.product_name,
                     quantity=item.quantity,
                     price=item.price,
                     product_id=item.product_id,
                     total_price=total_price,
                     )
        ).returning(CartItems)
        rs = session.execute(stmt).fetchone()
        return rs

    def get_cart_item_by_id_repo(self, cart_items_id: int) -> Row:
        session: Session = SessionLocal()
        stmt = (
            select(CartItems).where(CartItems.cart_items_id == cart_items_id)
        )
        rs = session.execute(stmt).fetchone()
        return rs

    def delete_items_in_cart_items_repo(self, customer_id: int) -> List[Row]:
        session: Session = SessionLocal()
        stmt = (
            delete(CartItems).join(Cart, Cart.customer_id).where(
                Cart.customer_id == customer_id)
        ).returning(CartItems)
        rs = session.execute(stmt).fetchone()
        return rs

    def delete_item_in_cart_items_repo(self, cart_item_id: int) -> Row:
        session: Session = SessionLocal()
        stmt = (
            delete(CartItems).where(
                CartItems.cart_items_id == cart_item_id
        ).returning(CartItems)
        )
        rs = session.execute(stmt).fetchone()
        session.commit()
        return rs
