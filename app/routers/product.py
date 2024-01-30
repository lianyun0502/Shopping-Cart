from fastapi import APIRouter


router = APIRouter(prefix="/products")

@router.post("")
async def add_product():
    '''
    Create Product API
    透過 body 傳入商品資訊, 並在資料庫中新增商品
    '''
    return {"message": "Create Product"}

@router.patch("/{product_id}")
async def update_product(product_id: int):
    '''
    Update Product API
    透過 Path 選擇商品，並根據body在資料庫中更新商品資訊，只能更新部分欄位
    '''
    return {"message": "Update Product"}

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    '''
    Delete Product API
    透過 Path 選擇商品，並在資料庫中刪除商品
    '''
    return {"message": "Delete Product"}

@router.get("")
async def get_all_products():
    '''
    Get All Products API
    取得所有商品資訊
    '''
    return {"message": "Get All Products"}

@router.get("/{product_id}")
async def get_product(product_id: int):
    '''
    Get Product API
    透過 Path 選擇商品，並取得商品資訊
    '''
    return {"message": "Get Product"}
