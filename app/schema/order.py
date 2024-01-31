from pydantic import BaseModel, Field
from time import time

class Order(BaseModel):
    user_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., example=1)


class OutOrder(BaseModel):
    id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., example=1)
    order_date: float = Field(time(), example=1)


class CreateOrder(Order):...




