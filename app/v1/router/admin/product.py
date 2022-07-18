from decimal import Decimal
from fastapi import APIRouter, Query
from starlette import status
from app.v1.service.admin.product import ProductService
from project.core.schemas import DataResponse, PageResponse
from project.core.schemas import Sort
from project.core.swagger import swagger_response
from schemas.product import ProductRes

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_400_BAD_REQUEST
    )
)
def get_product(
        page: int = Query(1, description="Page"),
        size: int = Query(10, description="Size in a page"),
        product_name: str = Query(None, description="Name product"),
        category: str = Query(None, description="Category"),
        product_id: int = Query(None, description="Product ID"),
        from_price: Decimal = Query(None, description="From price"),
        to_price: Decimal = Query(None, description="To price"),
        sort_direction: Sort.Direction = Query(None, description="Filter by")
) -> PageResponse:
    product_service = ProductService().get_product_service(
        page=page,
        size=size,
        product_id=product_id,
        category=category,
        product_name=product_name,
        from_price=from_price,
        to_price=to_price,
        sort_direction=sort_direction)

    return PageResponse(data=product_service.data,
                        total_page=product_service.total_page,
                        total_items=product_service.total_items,
                        current_page=product_service.current_page)
