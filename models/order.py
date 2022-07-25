from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DATE, MetaData
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base(metadata=MetaData(schema="ecommerce"))


class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer,
                      primary_key=True,
                      nullable=False)
    customer_id = Column(Integer,
                         ForeignKey("customers.customer_id"),
                         nullable=False)
    total_amount = Column(DECIMAL)
    status = Column(String)
    time_open = Column(DATE)



