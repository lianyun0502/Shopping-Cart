from pydantic import BaseModel, Field
from time import time
from datetime import datetime

class Order(BaseModel):
    user_id: str = Field(..., example="John Doe", max_length=50)
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., example=1)


class OutOrder(Order):
    id: int 
    order_date: datetime 


class CreateOrder(Order):...




