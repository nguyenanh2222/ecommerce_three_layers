import math

from fastapi import APIRouter, HTTPException
from starlette import status

from app.v1.repos.admin.order import OrderRepository
from order_status import EOrderStatus
from project.core.schemas import PageResponse, Sort, DataResponse

router = APIRouter()


class OrderService(OrderRepository):

    def get_order_service(self, page: int,
                          size: int, order_id: int,
                          product_name: str,
                          customer_name: str,
                          sort_direction: Sort.Direction) -> PageResponse:
        order_repo = OrderRepository().get_order_repo(
            page=page,
            size=size,
            order_id=order_id,
            product_name=product_name,
            customer_name=customer_name,
            sort_direction=sort_direction
        )

        total_page = math.ceil(len(order_repo) / size)
        total_items = len(order_repo)
        current_page = page

        if page and size is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return PageResponse(data=order_repo,
                            total_page=total_page,
                            total_items=total_items,
                            current_page=current_page)

    def change_order_service(self, order_id: int,
                             next_status: EOrderStatus) -> DataResponse:
        order_repo = OrderRepository().change_order_repo(
            order_id=order_id,
            next_status=next_status)
        return DataResponse(data=order_repo)


