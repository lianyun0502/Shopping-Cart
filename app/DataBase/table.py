from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True)
    email = Column(String(50))
    phone = Column(String(50))
    address = Column(String(50))
    cart_id = Column(Integer, unique=True)


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)
    description = Column(Text)
    quantity = Column(Integer)
    on_sale_date = Column(DateTime)


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    product_id = Column(Integer)
    quantity = Column(Integer)
    order_date = Column(DateTime)
    

class Carts(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)


class CartItems(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer)
    product_id = Column(Integer)
    quantity = Column(Integer)
    is_checked_out = Column(Boolean, default=False)




 
    