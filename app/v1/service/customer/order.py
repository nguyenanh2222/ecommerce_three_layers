from fastapi import HTTPException
from starlette import status
from app.v1.repos.customer.cart import CartRepository
from models.associations import CartItems
from schemas.associations import CartItemReq


class OrderService(CartRepository):

    def get_order_service(self, customer_id: int):
        cart = CartRepository().get_cart(customer_id=customer_id)
        if cart:
            cart_items = CartRepository().get_cart_items(cart_id=cart['cart_id'])
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        cart = {'customer_id': cart['customer_id'],
                'cart_id': cart['cart_id'],
                'cart_item': cart_items}
        return cart

    def change_item_in_cart_items_service(self, customer_id: int, item: CartItemReq):
        cart = CartRepository().get_cart(customer_id=customer_id)
        if cart:
            cart_id = cart['cart_id']
            total_price = item.price * item.quantity
            cart_items = CartRepository(
            ).add_item_to_cart_items(item=CartItems(cart_id=cart_id,
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
        if cart_items.get_cart_item_by_id(
                cart_items_id=cart_items_id):
            cart_items.delete_item_in_cart_items(
                cart_items_id=cart_items_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
