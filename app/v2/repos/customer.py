from typing import List

from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.cart import Cart
from models.customer import Customer
from schemas.customer import CustomerReq


class CustomerRepository:
    def create_profile_repo(self, customer: CustomerReq) -> Row:
        session = SessionLocal()
        stmt = session.insert(Customer).values(
            password=f'{customer.password}',
            name=f'{customer.name}',
            phone=f'{customer.phone}',
            address=f'{customer.address}',
            email=f'{customer.email}',
            username=f'{customer.username}'
        ).returning(Customer)
        rs = session.execute(stmt).fetchone()
        customer_id = rs['customer_id']
        session.commit()
        stmt = session.insert(Cart).values(customer={customer_id}).returning(Cart)
        session.execute(stmt)
        return rs

    def update_profile_repo(self, customer: CustomerReq, customer_id: int) -> Row:
        session = SessionLocal()
        query = f""" UPDATE customers
        SET phone = '{customer.phone}', name = '{customer.name}',
        address = '{customer.address}', email = '{customer.email}'
        WHERE customer_id = {customer_id} RETURNING * """
        rs = session.execute(query).fetchone()
        return rs

    def get_profile_repo(self, customer_id: int) -> List[Row]:
        session = SessionLocal()
        query = f"""SELECT * FROM customers 
        WHERE customer_id = {customer_id}"""
        rs = session.execute(query).fetchall()
        return rs