from typing import List

from sqlalchemy import select, insert, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from db.database import SessionLocal
from models.associations import CartItems
from models.cart import Cart


class CartRepository:
    def get_cart_repo(self, customer_id: int) -> Row:
        session: Session = SessionLocal()
        stmt = select(Cart).where(
            Cart.customer_id == customer_id)
        rs = session.execute(stmt).fetchone()
        return rs

    def get_cart_items_repo(self, cart_id: int) -> List[Row]:
        session: Session = SessionLocal()
        stmt = select(Cart, CartItems).where(
            Cart.customer_id == cart_id).join(Cart.cart_id).returning(Cart)
        rs = session.execute(stmt).fetchall()
        return rs

    def insert_item_to_cart_items_repo(
            self, item: CartItems) -> Row:
        session: Session = SessionLocal()
        stmt = (
            insert(CartItems).values(cart_id=item.cart_id,
                                     product_name=item.product_name,
                                     quantity=item.quantity,
                                     price=item.price,
                                     product_id=item.product_id,
                                     total_price=item.total_price)
        ).returning(CartItems)
        rs = session.execute(stmt).fetchone()
        return rs

    def update_item_in_cart_items_repo(self, item: CartItems,
                                       cart_item_id: int) -> Row:
        session: Session = SessionLocal()
        stmt = (
            update(CartItems).where(
                CartItems.cart_item_id == cart_item_id
            ).values(cart_id=item.cart_id,
                     price=item.price,
                     product_id=item.product_id,
                     quantity=item.quantity,
                     total_price=item.total_price,
                     product_name=item.product_name
                     )
        ).returning(CartItems)
        rs = session.execute(stmt).fetchone()
        return rs

    def get_cart_item_by_id_repo(self, cart_items_id):
        ...

    def delete_item_in_cart_items_repo(self, cart_items_id):
        pass
