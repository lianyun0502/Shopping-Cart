from pydantic import BaseModel, Field


class Cart(BaseModel):
    '''
    Cart Schema
    '''
    id : int = Field(..., example=1)


class CartItem(BaseModel):
    '''
    Cart Item Schema
    '''
    ...

class CreateCartItem(CartItem):
    '''
    Create Cart Item Schema
    '''
    cart_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., example=1)
    is_checked_out: bool = Field(..., example=True)


class UpdateCartItem(CartItem):
    '''
    Update Cart Item Schema
    '''
    quantity: int = Field(..., example=1)
    is_checked_out: bool = Field(..., example=True)


class OutCartItem(CartItem):
    '''
    Out Cart Item Schema
    '''
    id: int = Field(..., example=1)
    cart_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., example=1)
    is_checked_out: bool = Field(..., example=True)


