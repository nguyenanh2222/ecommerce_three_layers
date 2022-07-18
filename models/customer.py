from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DATE, MetaData
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base(metadata=MetaData(schema="ecommerce"))


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer,
                         primary_key=True,
                         nullable=False)
    password = Column(String(10))
    name = Column(String(50))
    phone = Column(String(10))
    address = Column(String(200))
    email = Column(String(100))
    username = Column(String(10))