from fastapi import APIRouter, Body
from starlette import status

from app.v1.repos.customer import CustomerRepository
from app.v1.service.customer.customer import CustomerService
from project.core.schemas import DataResponse
from project.core.swagger import swagger_response
from schemas.customer import CustomerReq, CustomerRes

router = APIRouter()


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_201_CREATED,
    )
)
def create_profile_service(customer: CustomerReq = Body(...)) -> DataResponse:
    customer = CustomerService().create_profile_service(customer=(CustomerReq(
        name=customer.name,
        phone=customer.phone,
        address=customer.address,
        email=customer.email,
        username=customer.username,
        password=customer.password)))
    return DataResponse(data=customer)


@router.put(
    path="/{customer_id}/profile",
    status_code=status.HTTP_200_OK,
    # deprecated=True,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_200_OK
    ))
def update_profile_router(customer: CustomerReq, customert_id: int) -> DataResponse:
    customers = CustomerRepository().update_profile_repo(customer=(CustomerReq(
        name=customer.name,
        phone=customer.phone,
        address=customer.address,
        email=customer.email,
        username=customer.username,
        password=customer.password)),
        customer_id=customert_id)
    return DataResponse(data=customers)


@router.get(
    path="/{customer_id}/profile",
    status_code=status.HTTP_200_OK,
    responses=swagger_response(
        response_model=DataResponse[CustomerRes],
        success_status_code=status.HTTP_200_OK)
)
def get_profile_service(customer_id: int) -> DataResponse:
    customers = CustomerRepository().get_profile_repo(customer_id=customer_id)
    return DataResponse(data=customers)
