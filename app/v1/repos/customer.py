from typing import List

from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.customer import CustomerReq


class CustomerRepository:
    def create_profile_repo(self, customer: CustomerReq) -> Row:
        session: Session = SessionLocal()
        query = f"""INSERT INTO customers (
        password, name, phone, address, email, username) 
        VALUES ( '{customer.password}','{customer.name}', '{customer.phone}', '{customer.address}',
        '{customer.email}' ,'{customer.username}') RETURNING *"""
        customer = session.execute(query).fetchone()
        customer_id = customer["customer_id"]
        query = f""" INSERT INTO cart (customer_id)
                    VALUES ({customer_id}) RETURNING *"""
        session.execute(query).fetchone()
        return customer

    def update_profile_repo(self, customer: CustomerReq, customer_id: int) -> Row:
        session: Session = SessionLocal()
        query = f""" UPDATE customers
        SET phone = '{customer.phone}', name = '{customer.name}',
        address = '{customer.address}', email = '{customer.email}'
        WHERE customer_id = {customer_id} RETURNING * """
        rs = session.execute(query).fetchone()
        return rs

    def get_profile_repo(self, customer_id: int) -> List[Row]:
        session: Session = SessionLocal()
        query = f"""SELECT * FROM customers 
        WHERE customer_id = {customer_id}"""
        rs = session.execute(query).fetchall()
        return rs