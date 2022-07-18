from fastapi import APIRouter
from app.v1.router.routers import Tags
from app.v1.service.admin.analysis import router as analysis_admin_router
from app.v1.service.admin.product import router as product_admin_router
from app.v1.service.admin.order import router as order_router

router_admin = APIRouter(prefix="/api/v1")
router_admin.include_router(router=analysis_admin_router, prefix="/admin/analysis", tags=[Tags.admin])
router_admin.include_router(router=product_admin_router, prefix="/products", tags=[Tags.admin])
router_admin.include_router(router=order_router, prefix="/orders", tags=[Tags.admin])
