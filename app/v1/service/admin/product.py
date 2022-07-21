import math
from decimal import Decimal

from fastapi import HTTPException
from starlette import status
from app.v1.repos.admin.product import ProductRepository
from project.core.schemas import Sort, PageResponse, DataResponse
from schemas.product import ProductReq


class ProductService(ProductRepository):

    def get_product_service(
            self, page: int, size: int, product_id: int,
            category: str, product_name: str,
            from_price: Decimal, to_price: Decimal,
            sort_direction: Sort.Direction) -> PageResponse:
        products = ProductRepository().get_products_repo(
            page=page,
            size=size,
            product_id=product_id,
            category=category,
            product_name=product_name,
            from_price=from_price,
            to_price=to_price,
            sort_direction=sort_direction)

        total_page = math.ceil(len(products) / size)
        total_items = len(products)
        current_page = page

        if page and size is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return PageResponse(data=products,
                            total_page=total_page,
                            total_items=total_items,
                            current_page=current_page)

    def get_product_by_id_service(self, product_id: int) -> DataResponse:
        product = ProductRepository().get_product_by_id_repos(
            product_id=product_id)
        return DataResponse(data=product)

    def put_product_service(self, product: ProductReq, product_id: int) -> DataResponse:
        product = ProductRepository().put_product_repos(
            product=product, product_id=product_id)
        return DataResponse(data=product)

    def post_product_service(self, product: ProductReq) -> DataResponse:
        product = ProductRepository().post_product_repos(
            product=product)
        return DataResponse(data=product)

    def delete_product_service(self, product_id: int) -> DataResponse:
        product = ProductRepository().delete_product_repos(product_id=product_id)
        return DataResponse(data=product)
