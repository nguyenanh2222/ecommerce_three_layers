from fastapi import HTTPException
from sqlalchemy.engine import Row
from starlette import status

from app.v1.repos.customer.cart import CartRepository
from models.associations import CartItems
from project.core.schemas import DataResponse
from schemas.associations import CartItemReq




class CartService(CartRepository):

    def get_cart_service(self, customer_id: int)-> DataResponse:
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
            total_price = item.price * item.quantity
            cart_items = CartRepository().insert_item_to_cart_items_repo(
                                                                 item=CartItems(
                                                                     cart_id=cart_id,
                                                                     product_name=item.product_name,
                                                                     quantity=item.quantity,
                                                                     price=item.price,
                                                                     product_id=item.product_id,
                                                                     total_price= total_price)
                                                                 )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def update_item_in_cart_items_service(self, customer_id: int, item: CartItemReq):
        cart = CartRepository().get_cart_repo(customer_id=customer_id)
        if cart:
            cart_id = cart['cart_id']
            total_price = item.price * item.quantity
            cart_items = CartRepository().update_item_in_cart_items_repo(
                                                                 item=CartItems(
                                                                     cart_id=cart_id,
                                                                     product_name=item.product_name,
                                                                     quantity=item.quantity,
                                                                     price=item.price,
                                                                     product_id=item.product_id,
                                                                     total_price=total_price)
                                                                 )
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    def delete_item_in_cart_items(self, cart_items_id: int):
        cart_items = CartRepository()
        if cart_items.get_cart_item_by_id_repo(cart_items_id=cart_items_id):
            cart_items.delete_item_in_cart_items_repo(cart_items_id=cart_items_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)



