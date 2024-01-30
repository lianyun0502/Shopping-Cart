from fastapi import APIRouter


router = APIRouter(prefix="/carts")

@router.post("/{cart_id}/items")
async def add_item(cart_id: int):
    '''
    Add Item to Cart API
    透過 Path 選擇購物車，並在資料庫中新增商品至購物車
    '''
    return {"message": "Add Item to Cart"}

@router.patch("/{cart_id}/items/{item_id}")
async def update_item(cart_id: int, item_id: int):
    '''
    Update Item in Cart API
    透過 Path 選擇購物車及商品，並根據body在資料庫中更新商品資訊，只能更新部分欄位
    '''
    return {"message": "Update Item in Cart"}


@router.delete("/{cart_id}/items/{item_id}")
async def delete_item(cart_id: int, item_id: int):
    '''
    Delete Item in Cart API
    透過 Path 選擇購物車及商品，並在資料庫中刪除商品
    '''
    return {"message": "Delete Item in Cart"}


@router.get("/{cart_id}/items")
async def get_all_items(cart_id: int):
    '''
    Get All Items in Cart API
    透過 Path 選擇購物車，並取得購物車中所有商品資訊
    '''
    return {"message": "Get All Items in Cart"}


@router.get("/{cart_id}/items/{item_id}")
async def get_item(cart_id: int, item_id: int):
    '''
    Get Item in Cart API
    透過 Path 選擇購物車及商品，並取得商品資訊
    '''
    return {"message": "Get Item in Cart"}


@router.get("")
async def get_all_carts():
    '''
    Get All Carts API
    取得所有購物車資訊
    '''
    return {"message": "Get All Carts"}


