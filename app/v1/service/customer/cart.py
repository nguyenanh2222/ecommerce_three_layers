from typing import List

from sqlalchemy.engine import Row

from app.v1.repos.customer.cart import CartRepository
from project.core.schemas import DataResponse


class CartService(CartRepository):

    def get_cart_service(self, customer_id: int):
        cart = CartRepository().get_cart(customer_id=customer_id)
        cart_items = CartService().get_cart_items(cart_id=cart['cart_id'])
        cart = {'customer_id': cart['customer_id'], 'cart_id': cart['cart_id'], 'cart_item': cart_items}
        return cart
