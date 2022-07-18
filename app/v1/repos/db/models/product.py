from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DATE, MetaData, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base(metadata=MetaData(schema="ecommerce"))


class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer,
                        primary_key=True,
                        nullable=False)
    description = Column(String(500))
    category = Column(String(200))
    name = Column(String(100))
    price = Column(DECIMAL)
    quantity = Column(Integer)
    created_time = Column(DATE,
                          default=func.now())
