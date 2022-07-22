from enum import Enum
from fastapi import APIRouter
from app.v1.router.admin.analysis import router as analysis_admin_router
from app.v1.router.admin.order import router as order_router
from app.v1.router.admin.product import router as product_admin_router
from app.v1.router.admin.permission import router as admin_permission_router
from app.v1.router.customer.cart import router as customer_cart_router
from app.v1.router.customer.order import router as customer_order_router
from app.v1.router.customer.customer import router as customer_profile_router


class Tags(str, Enum):
    customer = "[Customer]"
    admin = "[Admin]"
    customer_orm = "[Customer][ORM]"
    admin_orm = "[Admin][ORM]"


router_admin = APIRouter(prefix="/api/admin/v1")
router_admin.include_router(router=analysis_admin_router,
                            prefix="/analysis",
                            tags=[Tags.admin])
router_admin.include_router(router=order_router,
                            prefix="/orders",
                            tags=[Tags.admin])
router_admin.include_router(router=product_admin_router,
                            prefix="/products",
                            tags=[Tags.admin])
router_admin.include_router(router=admin_permission_router,
                            prefix="/permission",
                            tags=[Tags.admin])

router_customer = APIRouter(prefix="/api/customer/v1")
router_customer.include_router(router=customer_cart_router,
                               prefix="/carts",
                               tags=[Tags.customer])
router_customer.include_router(router=customer_order_router,
                               prefix="/orders",
                               tags=[Tags.customer])
router_customer.include_router(router=customer_profile_router,
                               prefix="/profiles",
                               tags=[Tags.customer])
