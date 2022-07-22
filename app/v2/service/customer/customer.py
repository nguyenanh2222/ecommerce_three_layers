from app.v2.repos.customer import CustomerRepository
from project.core.schemas import DataResponse
from schemas.customer import CustomerReq


class CustomerService(CustomerRepository):
    def create_profile_service(self, customer: CustomerReq) -> DataResponse:
        customer = CustomerRepository().create_profile_repo(customer=(CustomerReq(
            name=customer.name,
            phone=customer.phone,
            address=customer.address,
            email=customer.email,
            username=customer.username,
            password=customer.password)))
        return DataResponse(data=customer)

    def update_profile_service(self, customer: CustomerReq, customert_id: int) -> DataResponse:
        customers = CustomerRepository().update_profile_repo(customer=(CustomerReq(
                name=customer.name,
                phone=customer.phone,
                address=customer.address,
                email=customer.email,
                username=customer.username,
                password=customer.password)),
                customer_id=customert_id)

        return DataResponse(data=customers)

    def get_profile_service(self, customer_id: int) -> DataResponse:
        customers = CustomerRepository().get_profile_repo(customer_id=customer_id)
        return DataResponse(data=customers)

