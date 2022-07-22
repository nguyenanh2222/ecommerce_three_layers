from decimal import Decimal
from fastapi import APIRouter, Query, Depends
from starlette import status
from app.v2.router.admin.permission import get_user
from app.v2.service.admin.product import ProductService
from project.core.schemas import DataResponse, PageResponse
from project.core.schemas import Sort
from project.core.swagger import swagger_response
from schemas.product import ProductRes, ProductReq

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_404_NOT_FOUND
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
        sort_direction: Sort.Direction = Query(None, description="Filter by"),
        service: ProductService = Depends(get_user)
) -> PageResponse:
    products = ProductService().get_product_service(
        page=page,
        size=size,
        product_id=product_id,
        category=category,
        product_name=product_name,
        from_price=from_price,

        to_price=to_price,
        sort_direction=sort_direction)

    return PageResponse(data=products.data,
                        total_page=products.total_page,
                        total_items=products.total_items,
                        current_page=products.current_page)


@router.get(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_404_NOT_FOUND
    )
)
def get_product_by_id(product_id: int,
                      service: ProductService = Depends(get_user)) -> DataResponse:
    product = ProductService().get_product_by_id_service(
        product_id=product_id)
    return DataResponse(data=product)


@router.put(
    path="/{product_id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_400_BAD_REQUEST
    )
)
def put_product_by_id(product: ProductReq, product_id: int,
                      service: ProductService = Depends(get_user)) -> DataResponse:
    product = ProductService().put_product_service(
        product=product, product_id=product_id)
    return DataResponse(data=product)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,

    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_201_CREATED,
        fail_status_code=status.HTTP_400_BAD_REQUEST
    )
)
def post_product(product: ProductReq,
                 service: ProductService = Depends(get_user)) -> DataResponse:
    product = ProductService().post_product_service(
        product=product)
    return DataResponse(data=product)


@router.delete(
    path="/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(product_id: int,
                   service: ProductService = Depends(get_user)) -> DataResponse:
    product = ProductService().delete_product_service(product_id=product_id)
    return DataResponse(data=product)
