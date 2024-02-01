from pydantic import BaseModel, Field


class Cart(BaseModel):
    '''
    Cart Schema
    '''
    user_id : str = Field(..., example=1, max_length=50)


class OutCart(Cart):
    '''
    Out Cart Schema
    '''
    id: int 

class CreateCart(Cart):
    '''
    Create Cart Schema
    '''
    ...

class CartItem(BaseModel):
    '''
    Cart Item Schema
    '''
    ...

class CreateCartItem(CartItem):
    '''
    Create Cart Item Schema
    '''
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., example=1)
    is_checked_out: bool = Field(True, example=True)


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
    id: int 
    cart_id: int 
    product_id: int 
    quantity: int 
    is_checked_out: bool 


