import math
from fastapi import HTTPException
from starlette import status
from app.v1.repos.order import OrderRepository
from app.v1.repos.cart import CartRepository
from app.v1.repos.product import ProductRepository
from order_status import EOrderStatus
from project.core.schemas import Sort, PageResponse, DataResponse


class OrderService(CartRepository):

    def get_order_service(self, page: int,
                          size: int, order_id: int,
                          product_name: str,
                          customer_name: str,
                          sort_direction: Sort.Direction,
                          ) -> PageResponse:
        if page and size:
            orders = OrderRepository().get_order_repo(
                page=page,
                size=size,
                order_id=order_id,
                product_name=product_name,
                customer_name=customer_name,
                sort_direction=sort_direction
            )
            if orders['data'] == []:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return PageResponse(data=orders['data'],
                                total_page=orders['total_page'],
                                total_items=orders['total_items'],
                                current_page=orders['current_page'])
        if page and size is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )

    def change_status_service(self, order_id: int,
                              next_status: EOrderStatus) -> DataResponse:
        order = OrderRepository().change_status_repos(order_id=order_id,
                                                      next_status=next_status)
        return DataResponse(data=order)

    def place_order(self, customer_id: int):
        cart_id = CartRepository().get_cart_repo(
            customer_id=customer_id)['cart_id']
        if cart_id:
            order = OrderRepository().insert_order(
                customer_id=customer_id, cart_id=cart_id)
            if order:
                order_items = OrderRepository().insert_order_item(
                    order_id=order['order_id'])
                products_id = []
                for i in range(len(order_items)):
                    if order_items[i]['product_id'] not in products_id:
                        products_id.append(order_items[i]['product_id'])
                for product_id in products_id:
                    _product = ProductRepository().update_product_quantity(product_id=product_id)
                _cart_item = CartRepository().delete_item_in_cart_items_repository(customer_id=customer_id)

        # if cart_id:
        #
        #     if order:
        #
        #         print(order['order_id'])
        #
        #             if product_quantity:
        #                 del_cart_item = OrderRepository().delete_item_in_cart_items_repo(
        #                     customer_id=customer_id)
        # else:
        #     raise status.HTTP_404_NOT_FOUND
