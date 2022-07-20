from enum import Enum
from fastapi import APIRouter
from app.v1.router.admin.analysis import router as analysis_admin_router
from app.v1.router.admin.order import router as order_router
from app.v1.router.admin.product import router as product_admin_router
from app.v1.router.admin.permission import router as admin_permission_router


class Tags(str, Enum):
    customer = "[Customer]"
    admin = "[Admin]"
    customer_orm = "[Customer][ORM]"
    admin_orm = "[Admin][ORM]"


router_admin = APIRouter(prefix="/api/v1")
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
