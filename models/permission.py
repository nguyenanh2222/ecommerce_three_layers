from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base(metadata=MetaData(schema="ecommerce"))


class Permission(Base):
    __tablename__ = "permission"
    id = Column(Integer,
                primary_key=True,
                nullable=False)
    user_name = Column(String)
    password = Column(Integer)
    # 1: admin
    # 2: customer
