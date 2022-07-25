from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DATE, MetaData
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base(metadata=MetaData(schema="ecommerce"))


class Cart(Base):
    __tablename__ = "cart"

    customer_id = Column(Integer,
                         ForeignKey("customers.customer_id"),
                         nullable=False)
    cart_id = Column(Integer,
                     primary_key=True,
                     nullable=False)



