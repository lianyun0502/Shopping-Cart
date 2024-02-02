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
    from DataBase.base import SessionLocal, Base
    from DataBase import table
    # with SessionLocal() as db:

    #     users = [
    #         table.Users(id="Eric", email="eric@mail.com", phone="0912345670", address="Taipei"),
    #         table.Users(id="Tom", email="tome@mail.com", phone="0912345671", address="Taipei"),
    #         table.Users(id="Mary", email="mary@mail.com", phone="0912345672", address="Taipei"),
    #     ]
    #     db.add_all(users)
    #     db.commit()

    #     carts = [
    #         table.Carts(user_id="Eric"),
    #         table.Carts(user_id="Tom"),
    #         table.Carts(user_id="Mary"),
    #     ]
    #     db.add_all(carts)
    #     db.commit()

    #     products = [
    #         table.Products(name="Apple", price=10, description="From Taiwan", investory=100, user_id="Eric"),
    #         table.Products(name="Banana", price=20, description="From Taiwan", investory=100, user_id="Eric"),
    #         table.Products(name="Carrot", price=30, description="From Taiwan", investory=100, user_id="Eric"),
    #     ]

    #     db.add_all(products)
    #     db.commit()

    uvicorn.run(app='main:app', host="127.0.0.1", port=5000, reload=True)


