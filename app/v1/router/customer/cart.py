from typing import List
from fastapi import APIRouter
from starlette import status
from app.v1.service.customer.cart import CartService
from schemas.associations import CartItemReq

router = APIRouter()


@router.get(
    path="/carts",
    status_code=status.HTTP_200_OK
)
def get_cart(customer_id: int) -> List:
    cart = CartService().get_cart_service(customer_id=customer_id)
    return cart

@router.post(
    path="/cart",
    status_code=status.HTTP_201_CREATED
)
def post_item_in_cart_items(customer_id: int, item: CartItemReq):
    cart_item = CartService().insert_item_in_cart_items_service(
        customer_id=customer_id,
        item=CartItemReq(
            cart_items_id=item.cart_items_id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price,
            product_id=item.product_id
        )
    )
    return cart_item


@router.put(
    path="/cart",
    status_code=status.HTTP_200_OK
)
def put_item_in_cart_items(customer_id: int, item: CartItemReq):
    cart_item = CartService().update_item_in_cart_items_service(
        customer_id=customer_id,
        item=CartItemReq(
            cart_items_id=item.cart_items_id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price,
            product_id=item.product_id
        )
    )
    return cart_item

@router.delete(
    path="/cart",
    status_code=status.HTTP_200_OK
)
def delete_item_in_cart_item(cart_items_id: int):
    cart_item = CartService().delete_item_in_cart_items(
        cart_items_id=cart_items_id)
    return cart_item
