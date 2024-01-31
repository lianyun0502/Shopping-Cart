from fastapi import APIRouter, Body
from schema import product
from typing import List


router = APIRouter(prefix="/products", tags=["Product"])

@router.post("", response_model=product.OutProduct)
async def add_product(product: product.Product=Body(...)):
    '''
    Create Product API
    透過 body 傳入商品資訊, 並在資料庫中新增商品
    '''
    return {"message": "Create Product"}

@router.put("/{product_id}", response_model=product.OutProduct)
async def update_product(product_id: int, product: product.UpdateProduct=Body(...)):
    '''
    Update Product API
    透過 Path 選擇商品，並根據body在資料庫中更新商品資訊，只能更新部分欄位
    '''
    return {"message": "Update Product"}

@router.delete("/{product_id}", response_model=product.OutProduct)
async def delete_product(product_id: int, product: product.Product=Body(...)):
    '''
    Delete Product API
    透過 Path 選擇商品，並在資料庫中刪除商品
    '''
    return {"message": "Delete Product"}

@router.get("", response_model=List[product.OutProduct])
async def get_all_products():
    '''
    Get All Products API
    取得所有商品資訊
    '''
    return {"message": "Get All Products"}

@router.get("/", response_model=product.OutProduct)
async def get_product(product_id: int):
    '''
    Get Product API
    透過 Path 選擇商品，並取得商品資訊
    '''
    return {"message": "Get Product"}
