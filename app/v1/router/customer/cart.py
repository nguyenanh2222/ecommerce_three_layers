from typing import List

from fastapi import APIRouter
from starlette import status

from app.v1.service.customer.cart import CartService
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response
from schemas.cart import CartReq

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK
)
def get_cart(customer_id: int) -> List:
    cart = CartService().get_cart_service(customer_id=customer_id)
    return cart
