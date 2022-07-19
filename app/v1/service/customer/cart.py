from fastapi import APIRouter, Body, Query, HTTPException
from sqlalchemy.engine import CursorResult
from starlette import status
from db.database import SessionLocal
from schemas.associations import CartItemReq
from schemas.cart import CartRes
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response

router = APIRouter()


@router.get(
    path="/",
    description="Get giỏ hàng của customer",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
# get cart and cart_items
async def get_cart(customer_id: int = Query(...)):
    session = SessionLocal()
    query = f""" 
    SELECT * FROM ecommerce.customers c JOIN ecommerce.cart ca 
    ON c.customer_id = ca.customer_id 
    WHERE c.customer_id = {customer_id}"""
    _rs: CursorResult = session.execute(query)
    result = _rs.fetchall()
    _rs: CursorResult = session.execute(f""" 
        SELECT * FROM ecommerce.customers c 
        JOIN ecommerce.cart ca 
        ON c.customer_id = ca.customer_id 
        JOIN ecommerce.cart_items ci
        ON ca.cart_id = ci.cart_id
        WHERE c.customer_id = {customer_id}""")
    items = _rs.fetchall()
    if items == None:
        return DataResponse(data=result)
    if items != None:
        result = items
        return DataResponse(data=result)


@router.put(
    path="/items",
    description="Add Item To Cart",
    responses=swagger_response(
        response_model=DataResponse[CartRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def add_item_to_cart(
        customer_id: int = Query(...),
        item: CartItemReq = Body(...)
):
    session = SessionLocal()

    _rs: CursorResult = session.execute(f"""SELECT * FROM ecommerce.customers c
    JOIN ecommerce.cart ca ON c.customer_id = ca.customer_id 
    WHERE ca.customer_id = {customer_id}""")
    if _rs.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    _rs: CursorResult = session.execute(f"""INSERT INTO cart (customer_id) 
    VALUES ({customer_id}) """)
    _rs_cart: CursorResult = session.execute(f"""
    SELECT cart_id FROM cart WHERE customer_id = {customer_id}""")
    _cart_id = int(_rs_cart.fetchone()[0])
    _item: CursorResult = session.execute(f"""INSERT INTO cart_items 
        (product_name, cart_id, quantity, total_price, price, product_id) 
        VALUES ('{item.product_name}', {_cart_id}, 
        {item.quantity}, {item.quantity * item.price},
        {item.price}, {item.product_id}) RETURNING *""")
    result = _item.fetchone()
    session.commit()
    return DataResponse(data=result)

