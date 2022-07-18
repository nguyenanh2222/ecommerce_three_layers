from datetime import datetime
from fastapi import APIRouter
from fastapi.params import Query
from starlette import status
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
def revenue(time_started: datetime = Query(datetime.strptime(
        "2021-11-29", "%Y-%m-%d")),
        time_ended: datetime = Query(datetime.strptime(
        "2021-11-29", "%Y-%m-%d"))) -> DataResponse:
    analysis_service = AnalysisService().service_revenue(
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
def line_char(
        start_datetime: datetime = Query(
            datetime.strptime("2021-11-29", "%Y-%m-%d")),
        end_datetime: datetime = Query(
            datetime.strptime("2021-11-29", "%Y-%m-%d"))
) -> DataResponse:
    _rs = AnalysisService().service_line_char(
        start_time=start_datetime,
        end_time=end_datetime)
    return DataResponse(data=_rs)
