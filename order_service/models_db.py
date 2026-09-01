from sqlalchemy import Column, Integer, JSON
from order_service.database import Base

class OrderDB(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key = True)
    customer_id = Column(Integer, nullable = False)
    items = Column(JSON, nullable = False)