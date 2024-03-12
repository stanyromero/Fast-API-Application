from db.database import Base
from sqlalchemy import Integer,Column
class Sales(Base):
    __tablename__='sales_report'
    sale_id=Column(Integer,primary_key=True)
    customer_id=Column(Integer,nullable=False)
    item_id=Column(Integer,nullable=False)
    quantity=Column(Integer,nullable=False)