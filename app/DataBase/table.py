from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from .base import Base, engine

class Users(Base):
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True)
    email = Column(String(50))
    phone = Column(String(50))
    address = Column(String(50))
    cart_id = Column(Integer, unique=True, foreign_key='carts.id')

    cart = relationship('Carts', back_populates='user')


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
    user_id = Column(String(50), foreign_key='users.id')
    product_id = Column(Integer, foreign_key='products.id')
    quantity = Column(Integer)
    order_date = Column(DateTime)

    user = relationship('Users', back_populates='orders')
    product = relationship('Products', back_populates='orders')
    

class Carts(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)

    user = relationship('Users', back_populates='cart')


class CartItems(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, foreign_key='carts.id')
    product_id = Column(Integer, foreign_key='products.id')
    quantity = Column(Integer)
    is_checked_out = Column(Boolean, default=True)

    cart = relationship('Carts', back_populates='cart_items')
    product = relationship('Products', back_populates='cart_items')



Base.metadata.create_all(bind=engine)

Session:sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close_all()
    