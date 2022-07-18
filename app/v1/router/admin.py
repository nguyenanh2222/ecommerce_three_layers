from fastapi import APIRouter
from starlette import status
from dependency_injector.wiring import Provide, inject
from app.v1.service.schemas.product import ProductRes
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response

router = APIRouter()


@inject
@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=DataResponse[ProductRes],
        success_status_code=status.HTTP_201_CREATED
    )
)
async def create_product():
    ...
#     product_create: ProductRes
#     product_service: ProductRes = Depends(Provide[Container.product_service]))
# ):
#     return await product_service.mg_create(user_create)
