from fastapi import APIRouter, Body, Path
from pydantic import BaseModel, Field
from sqlalchemy.engine import CursorResult
from starlette import status

from app.v1.repos.db.database import SessionLocal
from app.v1.service.schemas.customer import CustomerRes, CustomerReq, CustomerUpdate
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response





router = APIRouter()


@router.post(
    path="/",

    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_201_CREATED,
    )
)
async def create_customer(customer: CustomerReq = Body(...)):
    session = SessionLocal()
    #ma hoa password trước khi nhận
    _rs: CursorResult = session.execute(
        f"""INSERT INTO customers (password, name, phone, address, email, username) 
        VALUES ( '{customer.password}','{customer.name}', '{customer.phone}', '{customer.address}',
        '{customer.email}' ,'{customer.username}') RETURNING *"""
    )
    _customer_id = _rs.first()[0]
    print(_customer_id)
    _rs: CursorResult = session.execute(
        f"""INSERT INTO cart (customer_id) VALUES({_customer_id})"""
    )
    session.commit()
    return DataResponse(data=status.HTTP_201_CREATED)


@router.put(
    path="/{customer_id}/profile",
    status_code=status.HTTP_200_OK,
    deprecated=True,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def update_profile(customer_id: int, customer: CustomerUpdate):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f"""UPDATE customers
    SET phone = '{customer.phone}', name = '{customer.name}',
    address = '{customer.address}', email = '{customer.email}'
    WHERE customer_id = {customer_id} RETURNING *""")
    _result = _rs.fetchone()
    session.commit()
    return DataResponse(data=_result)


@router.get(
    path="/{customer_id}/profile",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_200_OK
    )
)
async def get_profile(customer_id: int = Path(...)):
    session = SessionLocal()
    _rs: CursorResult = session.execute(f""" SELECT * FROM customers
    WHERE customer_id = {customer_id} 
    """)
    return DataResponse(data=_rs.first())
