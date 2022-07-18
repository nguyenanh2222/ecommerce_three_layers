from fastapi import APIRouter
from app.v1.router.routers import Tags
from app.v1.service.customer.customer import router as product_customer_router
from app.v1.service.customer.order import router as customer_order_router
from app.v1.service.customer.order import router as customer_order_items_router
from app.v1.service.customer.customer import router as customers_router
# from app.v1.service.customer.cart import router as cart_router

router_customer = APIRouter(prefix="/api/v1")

router_customer.include_router(router=product_customer_router, prefix="/customer/products", tags=[Tags.customer])
router_customer.include_router(router=customer_order_router, prefix="/customers/orders", tags=[Tags.customer])
# router_customer.include_router(router=cart_router, prefix="/customers/cart", tags=[Tags.customer])
router_customer.include_router(router=customer_order_items_router, prefix="/customers/orders", tags=[Tags.customer])
router_customer.include_router(router=customers_router, prefix="/customers", tags=[Tags.customer])
