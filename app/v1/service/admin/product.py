from decimal import Decimal
from fastapi import APIRouter, Body, Query
from sqlalchemy.engine import CursorResult, Row
from starlette import status
from app.v1.repos.db.database import SessionLocal
from app.v1.service.customer.product import ProductReq
from app.v1.service.schemas.product import ProductRes
from project.core.schemas import DataResponse, PageResponse
from project.core.schemas import Sort
from project.core.swagger import swagger_response
import math



router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def create_product(product: ProductReq = Body(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(
        f"""INSERT INTO ecommerce.products (name, quantity, price, description, category, created_time) 
        VALUES ('{product.name}', {product.quantity}, {product.price},
                '{product.description}', '{product.category}', '{product.created_time}') RETURNING *"""
    )
    session.commit()
    return DataResponse(data=_rs.first())


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=PageResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_products(
        page: int = Query(1, description="Page"),
        size: int = Query(20, description="Size in a page"),
        name: str = Query(None, description="Name product"),
        category: str = Query(None, description="Category"),
        product_id: int = Query(None, description="Product ID"),
        from_price: Decimal = Query(None, description="From price"),
        to_price: Decimal = Query(None, description="To price"),
        sort_direction: Sort.Direction = Query(None, description="Filter by")
):
    query = "SELECT * FROM ecommerce.products"
    parameters = [name, category, product_id, from_price, to_price]
    for parameter in parameters:
        if parameter is not None:
            query += " WHERE "
            break
    if name is not None:
        query += f" name LIKE '%{name}%' AND"
    if category is not None:
        query += f" category LIKE '%{category}%' AND"
    if product_id is not None:
        query += f" product_id = {product_id} AND"
    if from_price is not None:
        query += f" price >= {from_price} AND"
    if to_price is not None:
        query += f" price <= {to_price} AND"
    if query.endswith("AND"):
        query = query[:-3]
    if sort_direction is not None:
        query += f""" ORDER BY created_time {sort_direction}"""

    session = SessionLocal()
    _rs: CursorResult = session.execute(query)
    total = _rs.fetchall()
    total_page = math.ceil(len(total) / size)
    total_items = len(total)
    query += f" LIMIT {size} OFFSET {(page - 1) * size}"
    _rs: CursorResult = session.execute(query)
    _result = _rs.fetchall()
    current_page = page
    return PageResponse(data=_result,
                        total_page=total_page,
                        total_items=total_items,
                        current_page=current_page)


@router.get(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_product(id: int):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f'SELECT * FROM products WHERE product_id = {id}')
    product: Row = _rs.first()
    return DataResponse(data=product)


@router.put(
    path="/{id}",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def update_product(id: int, product: ProductReq):
    session = SessionLocal()
    _rs = session.execute(
        f""" UPDATE products
        SET description = '{product.description}', 
        category = '{product.category}', name = '{product.name}', 
        price = {product.price}, quantity = {product.quantity}, 
        created_time = '{product.created_time}' 
        WHERE product_id = {id} RETURNING *""")
    session.commit()
    return DataResponse(data=_rs.first())


@router.delete(
    path="/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(id_: int = Query(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f'DELETE FROM products WHERE product_id = {id_}')
    session.commit()
    return DataResponse(data=None, status_code=status.HTTP_204_NO_CONTENT)
