import uvicorn

from enum import Enum
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ecommerce_three_layers",
    description="Ecommerce Description",
    debug=True,
    version="0.0.2",
    docs_url="/",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse
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


router = APIRouter(prefix="/api/v1")

# router.include_router(router=admin_router.router)


if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8001, reload=True)