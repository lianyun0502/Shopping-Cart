from fastapi import APIRouter


router = APIRouter(prefix="/users")


@router.post("")
async def create_user():
    '''
    Create User API
    透過 body 傳入使用者資訊, 並在資料庫中新增使用者
    '''
    return {"message": "Create User"}

@router.patch("/{user_id}")
async def update_user(user_id: str):
    '''
    Update User API
    透過 Path 選擇使用者，並根據body在資料庫中更新使用者資訊，只能更新部分欄位
    '''
    return {"message": "Update User"}