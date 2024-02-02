from pydantic import BaseModel, Field
from time import time
from datetime import datetime

class Order(BaseModel):
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., example=1)


class OutOrder(Order):
    id: int 
    user_id: str
    order_date: datetime 


class CreateOrder(Order):...




