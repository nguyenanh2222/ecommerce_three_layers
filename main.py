import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.v1.router.routers import router_admin
from app.v1.router.routers import router_customer
from app.v2.router.routers import router_admin_orm
from app.v2.router.routers import router_customer_orm

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

app.include_router(router_admin)
app.include_router(router_customer)
app.include_router(router_admin_orm)
app.include_router(router_customer_orm)
if __name__ == "__main__":
    uvicorn.run('main:app',
                host="127.0.0.1",
                port=8001,
                reload=True)