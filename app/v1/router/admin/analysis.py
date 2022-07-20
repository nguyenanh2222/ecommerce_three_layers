from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.params import Query
from starlette import status

from app.v1.router.admin.permission import get_user
from app.v1.service.admin.analysis import AnalysisService
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response

router = APIRouter()


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    description="get revenue by time",
    responses=swagger_response(
        response_model=DataResponse,
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_404_NOT_FOUND
    )
)
def get_revenue(time_started: datetime = Query(datetime.strptime(
        "2021-11-29", "%Y-%m-%d")),
        time_ended: datetime = Query(datetime.strptime(
        "2021-11-29", "%Y-%m-%d")),
        service: AnalysisService = Depends(get_user)) -> DataResponse:
    analysis_service = AnalysisService().calculate_revenue(
        start_time=time_started,
        end_time=time_ended)
    return DataResponse(data=analysis_service)

@router.get(
    path="/linechart",
    status_code=status.HTTP_200_OK,
    description="Draw line chart calculate amount total",
    responses=swagger_response(
        response_model=DataResponse,
        success_status_code=status.HTTP_200_OK,
        fail_status_code=status.HTTP_404_NOT_FOUND
    )
)
def get_chart(
        start_datetime: datetime = Query(
            datetime.strptime("2021-11-29", "%Y-%m-%d")),
        end_datetime: datetime = Query(
            datetime.strptime("2021-11-29", "%Y-%m-%d")),
        service: AnalysisService = Depends(get_user)) -> DataResponse:
    analysis_service = AnalysisService().draw_chart(
        start_datetime=start_datetime,
        end_datetime=end_datetime)
    return DataResponse(data=analysis_service)
