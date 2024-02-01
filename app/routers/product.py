from fastapi import APIRouter, Body, Depends, HTTPException
from schema import product
from typing import List
from DataBase import table
from DataBase.base import get_db, Session


router = APIRouter(prefix="/products", tags=["Product"])

@router.post("", response_model=product.OutProduct)
async def add_product(product: product.CreateProduct=Body(...),
                      db:Session=Depends(get_db)
                      ):
    '''
    Create Product API
    透過 body 傳入商品資訊, 並在資料庫中新增商品
    '''
    product = table.Products(**product.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/", response_model=product.OutProduct)
async def update_product(product_id: int, 
                         product: product.UpdateProduct=Body(...), 
                         db:Session=Depends(get_db)
                         ):
    '''
    Update Product API
    透過 Path 選擇商品，並根據body在資料庫中更新商品資訊，只能更新部分欄位
    '''
    
    db.query(table.table.Products).filter(table.Products.id == product_id).update(product.model_dump())
    db.commit()
    out_product = db.query(table.Products).filter(table.Products.id == product_id).scalar()
    return out_product

@router.delete("/", response_model=product.OutProduct)
async def delete_product(product_id: int,  
                         db:Session=Depends(get_db)):
    '''
    Delete Product API
    透過 Path 選擇商品，並在資料庫中刪除商品
    '''
    product = db.query(table.Products).filter(table.Products.id == product_id).scalar()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return product

@router.get("", response_model=List[product.OutProduct])
async def get_all_products(skip: int = 0, limit: int = 100, db:Session=Depends(get_db)):
    '''
    Get All Products API
    取得所有商品資訊
    '''
    products = db.query(table.Products).offset(skip).limit(limit).all()
    return products

@router.get("/", response_model=product.OutProduct)
async def get_product(product_id: int, db:Session=Depends(get_db)):
    '''
    Get Product API
    透過 Path 選擇商品，並取得商品資訊
    '''
    product = db.query(table.Products).filter(table.Products.id == product_id).scalar()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
