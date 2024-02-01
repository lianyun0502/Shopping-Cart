from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class Product(BaseModel):
    '''
    Product Schema
    '''
    name: str = Field(..., example="iPhone 12", max_length=50)
    description: str = Field(..., example="Apple iPhone 12 128G 6.1吋 5G智慧型手機")
    price: int = Field(..., example=28500)

class CreateProduct(Product):
    '''
    Create Product Schema
    '''
    investory: int = Field(..., example=10)


class OutProduct(Product):
    '''
    Out Product Schema
    '''
    id: int 
    investory: int 
    on_sale_date: datetime 

class UpdateProduct(Product):
    '''
    Update Product Schema
    '''
    investory: int = Field(..., example=10)

