from pydantic import BaseModel


class Customer(BaseModel): #Serializer
    customer_id:int
    customer_name:str
    phone_number:str
    
    class Config:
        orm_mode=True