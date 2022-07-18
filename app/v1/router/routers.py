from enum import Enum
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.v1.router.admin.analysis import router as analysis_admin_router
from app.v1.router.admin.order import router as order_router
from app.v1.router.admin.product import router as product_admin_router
# from app.v1.service.admin.analysis import AnalysisService
# from project.core.schemas import DataResponse
# from project.core.swagger import swagger_response

app = FastAPI(
    title="Ecommerce Description",
    description="Ecommerce Description",
    debug=True,
    version="0.0.2",
    docs_url="/",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["POST", "GET"],
)



class Tags(str, Enum):
    customer = "[Customer]"
    admin = "[Admin]"
    customer_orm = "[Customer][ORM]"
    admin_orm = "[Admin][ORM]"


router = APIRouter()
router_admin = APIRouter(prefix="/api/v1")
router_admin.include_router(router=analysis_admin_router, prefix="/analysis", tags=[Tags.admin])
router_admin.include_router(router=order_router, prefix="/orders", tags=[Tags.admin])
router_admin.include_router(router=product_admin_router, prefix="/products", tags=[Tags.admin])
