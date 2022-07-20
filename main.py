import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.v1.router.routers import router_admin
from app.v1.router.routers import router_customer

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
if __name__ == "__main__":
    uvicorn.run('main:app',
                host="127.0.0.1",
                port=8001,
                reload=True)