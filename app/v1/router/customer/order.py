from fastapi import APIRouter, Query, Depends
from starlette import status

from app.v1.router.admin.permission import get_user
from app.v1.service.customer.order import OrderService
from order_status import EOrderStatus
from project.core.schemas import DataResponse, PageResponse, Sort
from project.core.swagger import swagger_response
from schemas.order import OrderRes

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=PageResponse[OrderRes],
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_404_NOT_FOUND
    )
)
def get_order(
        page: int = Query(1, description="Page Number"),
        size: int = Query(10, description="Page Size"),
        order_id: int = Query(None, description="Order ID"),
        product_name: str = Query(None, description="Product Name"),
        customer_name: str = Query(None, description="Customer Name"),
        sort_direction: Sort.Direction = Query(None, description="Sort By Time"),
        # _authorization: Optional[str] = Header(None),
        service=Depends(get_user)
) -> PageResponse:
    orders = OrderService().get_order_service(
        page=page,
        size=size,
        order_id=order_id,
        product_name=product_name,
        customer_name=customer_name,
        sort_direction=sort_direction
    )
    return PageResponse(
        data=orders.data,
        total_page=orders.total_page,
        total_items=orders.total_items,
        current_page=orders.current_page
    )

@router.put(
    path="/{order_id}",
    description="Get Order By ID",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse,
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_404_NOT_FOUND
    )

)
def change_order(order_id: int,
                 next_status: EOrderStatus,
                 service=Depends(get_user)) -> DataResponse:
    order = OrderService().change_order_service(
        order_id=order_id,
        next_status=next_status)
    return DataResponse(data=order)
