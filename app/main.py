from fastapi import FastAPI
from routers import cart, order, product, user

app = FastAPI(  
    title="Shopping Cart API",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="1.0.0",
    debug=True,
)

routers = [cart.router, order.router, product.router, user.router]
for router in routers:
    app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/login")
async def login():
    '''
    Login API
    預設透過 form data 傳遞帳號密碼, 並回傳 token 或 cookie 
    '''
    return {"message": "Login"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)


