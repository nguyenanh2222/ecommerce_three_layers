import uvicorn

from app.v1.router.admin import router_admin
from app.v1.router.customer import router_customer
from app.v1.router.routers import app

app.include_router(router_admin)
app.include_router(router_customer)
if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=8001, reload=True)