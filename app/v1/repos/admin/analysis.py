from datetime import datetime
from typing import List
from sqlalchemy.engine import CursorResult, Row
from sqlalchemy.orm import Session
from db.database import SessionLocal


class AnalysisRepository:

    def calculate_revenue(self,
                      start_time: datetime,
                      end_time: datetime) -> List[Row]:
        # sum, avg group by max and min by period time
        session: Session = SessionLocal()
        query = f"""
    SELECT SUM (total_amount), AVG(total_amount),
    MAX(customer_id), MAX(order_id) 
    FROM ecommerce.orders o
    WHERE time_open >= '{start_time}' 
    AND time_open <= '{end_time}'
    GROUP BY order_id """
        rs = session.execute(query).fetchall()
        return rs

    def draw_chart(self, start_datetime: datetime,
                         end_datetime: datetime) -> List[Row]:
        # draw line char calculate total amount by period time
        session: Session = SessionLocal()
        query = f"""
    SELECT time_open, SUM(total_amount) 
    FROM ecommerce.orders
    WHERE time_open >= '{start_datetime}'
    AND time_open <= '{end_datetime}'
    GROUP BY time_open"""
        rs = session.execute(query).fetchall()
        return rs
