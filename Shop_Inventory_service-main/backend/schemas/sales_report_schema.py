from pydantic import BaseModel


class Sales(BaseModel): #Serializer
    sale_id:int
    customer_id:int
    item_id:int
    quantity:int
    
    class Config:
        orm_mode=True