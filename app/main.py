from fastapi import FastAPI, Depends
from typing import Annotated, Optional
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from routers import cart, order, product, user, auth



app = FastAPI(  
    title="Shopping Cart API",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0.0",
    debug=True,
)

routers = [auth.router, user.router, cart.router, order.router, product.router]
for router in routers:
    app.include_router(router)


@app.get("/", response_class=PlainTextResponse)
async def root():
    return f"Welcome to Shopping Cart API"



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app='main:app', host="127.0.0.1", port=5000, reload=True)


