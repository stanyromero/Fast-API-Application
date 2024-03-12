from pydantic import BaseModel


class Item(BaseModel): #Serializer
    id:int
    name:str
    description:str
    price:int
    on_offer:bool
    in_stock:int
    
    class Config:
        orm_mode=True