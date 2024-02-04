from fastapi import APIRouter, Body, Depends, HTTPException
from schema import product
from typing import List, Optional
from DataBase import table
from DataBase.base import get_db, Session


router = APIRouter(prefix="/products", tags=["Product"])

def is_user_exist(user_id:str, db:Session)->Optional[table.Users]:
    user = db.query(table.Users).filter(table.Users.id == user_id).scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("{user_id}", response_model=product.OutProduct)
async def add_product(
    user_id: str,
    product: product.CreateProduct=Body(...),
    db:Session=Depends(get_db)
    ):
    '''
    Create Product API

        根據 Path 選擇使用者，並透過 body 傳入商品資訊, 並在資料庫中新增商品
    '''
    user = is_user_exist(user_id=user_id, db=db)
    product = table.Products(user_id=user_id, **product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/{user_id}", response_model=product.OutProduct)
async def update_product(
    user_id: str,
    product_id: int, 
    product: product.UpdateProduct=Body(...), 
    db:Session=Depends(get_db)
    ):
    '''
    Update Product API

        透過Path以及Query選擇使用者的商品，並根據body在資料庫中更新商品資訊，只能更新部分欄位
        會檢查使用者商品是否存在，若不存在則回傳 404, Product not found
        
    '''
    user = is_user_exist(user_id=user_id, db=db)
    query = db.query(table.Products).filter(table.Products.id == product_id and table.Products.user_id == user_id)
    query_product = query.scalar()    
    if query_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    query.update(product.model_dump())
    db.commit()
    db.refresh(query_product)
    # out_product = db.query(table.Products).filter(table.Products.id == product_id).scalar()
    return query_product

@router.delete("/{user_id}", response_model=product.OutProduct)
async def delete_product(
    user_id: str,   
    product_id: int,  
    db:Session=Depends(get_db)):
    '''
    Delete Product API
        透過 Path 選擇使用者商品，並在資料庫中刪除商品
    '''
    user = is_user_exist(user_id=user_id, db=db)
    query = db.query(table.Products)
    product = query.filter(table.Products.id == product_id and table.Users.id == user_id).scalar()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found") 
    db.delete(product)
    db.commit()
    return product

@router.get("", response_model=List[product.OutProduct])
async def get_all_products(user_id:Optional[str] = None ,skip: int = 0, limit: int = 100, db:Session=Depends(get_db)):
    '''
    Get All Products API

        取得所有商品資訊
        user_id: 選擇使用者，如果參數存在則取得該使用者的商品
    '''
    if user_id:
        user = is_user_exist(user_id=user_id, db=db)
        query = db.query(table.Products).join(table.Users, table.Products.user_id == table.Users.id).filter(table.Users.id == user_id)
        products = query.offset(skip).limit(limit).all()
    else:
        products = db.query(table.Products).offset(skip).limit(limit).all()
    return products

# @router.get("/", response_model=product.OutProduct)
# async def get_product(product_id: int, db:Session=Depends(get_db)):
#     '''
#     Get Product API
#     透過 Path 選擇商品，並取得商品資訊
#     '''
#     product = db.query(table.Products).filter(table.Products.id == product_id).scalar()
#     if product is None:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product
