from fastapi import APIRouter, Query
from starlette import status

from app.v1.repos.db.database import SessionLocal
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response
from datetime import datetime
from sqlalchemy.engine import CursorResult

router = APIRouter()


def repos_revenue():
    session = SessionLocal()
    query = f""" SELECT SUM(total_amount), AVG(total_amount),
    MAX(customer_id), MAX(order_id) 
    FROM ecommerce.orders o
    WHERE time_open >= '{start_datetime}' 
    AND time_open <= '{end_datetime}'
    GROUP BY order_id 
    """
    _rs: CursorResult = session.execute(query)


def service_revenue():
    rs = repos_revenue()
    # do st
    return rs

@router.get(
    path="/total",
    status_code=status.HTTP_200_OK,
    description="tính doanh thu theo một khoảng thời gian",
    responses=swagger_response(
        response_model=DataResponse,
        success_status_code=status.HTTP_200_OK
    )
)
async def analysis_revenue_in_period(
        start_datetime: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d")),
        end_datetime: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d"))
):
    _rs = service_revenue()

    return DataResponse(date=_rs.fetchall())



@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    description="line char",
    responses=swagger_response(
        response_model=DataResponse,
        success_status_code=status.HTTP_200_OK
    )
)
async def line_chart(
        day_started: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d")),
        day_ended: datetime = Query(datetime.strptime("2021-11-29", "%Y-%m-%d"))
):
    session = SessionLocal()
    query = f""" SELECT time_open, SUM(total_amount) FROM ecommerce.orders
    WHERE time_open >= '{day_started}'
    AND time_open <= '{day_ended}' 
    GROUP BY time_open
    """
    _rs: CursorResult = session.execute(query)
    result = _rs.fetchall()
    return DataResponse(data=result)
