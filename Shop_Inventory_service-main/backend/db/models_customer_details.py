from db.database import Base
from sqlalchemy import Integer,Column,String


class Customer(Base):
    __tablename__='customer_details'
    customer_id=Column(Integer,primary_key=True)
    customer_name=Column(String(255),nullable=False)
    phone_number=Column(String(255),nullable=False)
