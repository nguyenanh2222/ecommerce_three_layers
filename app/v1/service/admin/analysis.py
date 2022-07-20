from datetime import datetime
from fastapi import APIRouter
from app.v1.repos.admin.analysis import AnalysisRepository
from project.core.schemas import DataResponse


router = APIRouter()


class AnalysisService(AnalysisRepository):

    def service_revenue(self, start_time: datetime,
                        end_time: datetime) -> DataResponse:
        revenues = AnalysisRepository()
        revenues.calculate_revenue(
            start_time=start_time,
            end_time=end_time
        )
        return DataResponse(data=revenues)

    def service_draw_char(self,
                          start_time: datetime,
                          end_time: datetime) -> DataResponse:
        lines = AnalysisRepository().draw_chart(
            start_datetime=start_time,
            end_datetime=end_time)
        return DataResponse(data=lines)

