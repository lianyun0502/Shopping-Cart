from pydantic import BaseModel, Field, EmailStr
from time import time

class User(BaseModel):
    '''
    User Schema
    '''
    name: str = Field(..., example="John Doe", max_length=50)
    email: EmailStr = Field(..., example="a123456789@mail.com", max_length=50)
    phone: str = Field(..., example="0912345678",  max_length=50)
    address: str = Field(..., example="台北市大安區復興南路一段390號", max_length=50)
    

class CreateUser(User):
    '''
    Create User Schema
    '''
    ...


class OutUser(User):
    '''
    Out User Schema
    '''
    cart_id: int = Field(..., example=1)


