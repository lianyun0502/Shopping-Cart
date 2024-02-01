from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker, Session
from .base import Base, engine
from datetime import datetime

class Users(Base):
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True)
    email = Column(String(50))
    phone = Column(String(50))
    address = Column(String(50))

    orders = relationship('Orders')
    carts = relationship('Carts')


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    price = Column(Integer)
    description = Column(Text)
    investory = Column(Integer)
    on_sale_date = Column(DateTime, default=datetime.utcnow())
    
    orders = relationship('Orders')
    cart_items = relationship('CartItems')


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    order_date = Column(DateTime, default=datetime.utcnow())

    users = relationship('Users')
    products = relationship('Products')
    

class Carts(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey('users.id'))

    cart_items = relationship('CartItems')


class CartItems(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    is_checked_out = Column(Boolean, default=True)



Base.metadata.create_all(bind=engine)

SessionLocal:sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Dependency
def get_db():
    db:Session = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()
    