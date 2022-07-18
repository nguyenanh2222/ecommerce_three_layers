from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DATE, MetaData, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base(metadata=MetaData(schema="ecommerce"))


class CartItems(Base):
    __tablename__ = "cart_items"

    cart_id = Column(Integer,
                     ForeignKey("cart.cart_id"),
                     nullable=False)
    product_name = Column(String)
    cart_items_id = Column(Integer,
                           primary_key=True,
                           nullable=False)
    product_id = Column(Integer,
                        ForeignKey("products.product_id"),
                        nullable=False)
    total_price = Column(DECIMAL)
    quantity = Column(Integer)
    price = Column(DECIMAL)


class OrderItems(Base):
    __tablename__ = "order_items"
    product_id = Column(Integer,
                        ForeignKey("products.product_id"),
                        nullable=True
                        )

    product_name = Column(String)
    quantity = Column(Integer)
    price = Column(DECIMAL)
    total_price = Column(DECIMAL)
    order_id = Column(Integer,
                      ForeignKey("orders.order_id"),
                      nullable=True)
    order_items_id = Column(Integer,
                            primary_key=True,
                            nullable=False)
    product = relationship("Products")
