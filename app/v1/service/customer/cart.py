from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.engine import Row
from starlette import status

from app.v1.repos.cart import CartRepository
from app.v1.repos.product import ProductRepository
from models.associations import CartItems
from project.core.schemas import DataResponse
from schemas.associations import CartItemReq


class CartService(CartRepository):

    def get_cart_service(self, customer_id: int) -> DataResponse:
        cart = CartRepository().get_cart_repo(customer_id=customer_id)
        if cart:
            cart_items = CartRepository().get_cart_items_repo(cart_id=cart['cart_id'])
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        cart = {'customer_id': cart['customer_id'],
                'cart_id': cart['cart_id'],
                'cart_item': cart_items}
        return DataResponse(data=cart)

    def insert_item_in_cart_items_service(self, customer_id: int, item: CartItemReq):
        cart = CartRepository().get_cart_repo(customer_id=customer_id)
        if cart:
            cart_id = cart['cart_id']
            total_price = Decimal(item.price * item.quantity)
            item = CartRepository().insert_item_to_cart_items_repo(
                item=CartItems(
                    product_name=item.product_name,
                    quantity=item.quantity,
                    price=item.price,
                    product_id=item.product_id,
                ),
                cart_id=cart_id,
                total_price=total_price,

            )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def update_item_in_cart_items_service(self, customer_id: int,
                                          item: CartItemReq,
                                          cart_items_id: int):
        product = ProductRepository().get_product_by_id_repos(item.product_id)
        if product:
            cart = CartRepository().get_cart_repo(customer_id=customer_id)
            if cart:
                cart_id = cart['cart_id']
                total_price = Decimal(item.price * item.quantity)
                item = CartRepository().update_item_in_cart_items_repo(
                    item=CartItemReq(
                        product_name=item.product_name,
                        quantity=item.quantity,
                        price=item.price,
                        product_id=item.product_id
                    ),
                    cart_id=cart_id,
                    total_price=total_price,
                    cart_items_id=cart_items_id,
                )
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def delete_item_in_cart_items(self, cart_items_id: int):
        cart_items = CartRepository()
        if cart_items.get_cart_item_by_id_repo(cart_items_id=cart_items_id):
            cart_items.delete_item_in_cart_items_repo(cart_item_id=cart_items_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
