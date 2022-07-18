from datetime import datetime
from fastapi import APIRouter
from app.v1.repos.admin.analysis import AnalysisRepository
from project.core.schemas import DataResponse


router = APIRouter()


class AnalysisService(AnalysisRepository):

    def service_revenue(self, start_time: datetime,
                        end_time: datetime) -> DataResponse:
        analysis_repos = AnalysisRepository()
        analysis_repos.repos_revenue(
            start_time=start_time,
            end_time=end_time
        )
        return DataResponse(data=analysis_repos)

    def service_line_char(self,
                          start_time: datetime,
                          end_time: datetime) -> DataResponse:
        analysis_repos = AnalysisRepository().repos_line_chart(
            start_datetime=start_time,
            end_datetime=end_time)
        return DataResponse(data=analysis_repos)

