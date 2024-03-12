from fastapi import APIRouter,Form, status, HTTPException, UploadFile, File, Depends

from schemas.items_schema import Item
from schemas.sales_report_schema import Sales
from schemas.customer_schema import Customer

from typing import List
from db.database import SessionLocal
from db import models_items_in_stock, models_sales_report, models_customer_details
import pandas as pd
from sqlalchemy import desc
from sqlalchemy.orm import Session


router = APIRouter()


db=SessionLocal()

#For Manager

#To get all the items
@router.get('/items/getAll',response_model=List[Item],status_code=200,tags=["For Manager"])
def get_all_items():
    items=db.query(models_items_in_stock.Item).all()
    return items

#To get a specific item
@router.get('/item/get/specificItem/{item_id}',response_model=Item,status_code=status.HTTP_200_OK,tags=["For Manager"])
def get_an_item(item_id:int):
    item=db.query(models_items_in_stock.Item).filter(models_items_in_stock.Item.id==item_id).first()
    return item

#To get a specific item's stock
@router.get('/item/get/specificItem/stock/{item_id}',response_model=Item,status_code=status.HTTP_200_OK,tags=["For Manager"])
def get_an_item_stock(item_id:int):
    item=db.query(models_items_in_stock.Item).filter(models_items_in_stock.Item.id==item_id).first().in_stock
    return item

#To create a new item in the Database
@router.post('/items/create',response_model=Item,status_code=status.HTTP_201_CREATED,tags=["For Manager"])
def create_an_item(item:Item):
    db_item=db.query(models_items_in_stock.Item).filter(models_items_in_stock.Item.name==item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="Item already exists")

    new_item=models_items_in_stock.Item(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer,
        in_stock=item.in_stock
    )

    db.add(new_item)
    db.commit()

    return new_item

#To update a particular item
@router.put('/item/update/{item_id}',response_model=Item,status_code=status.HTTP_200_OK,tags=["For Manager"])
def update_an_item(item_id:int,item:Item):
    
    item_to_update=db.query(models_items_in_stock.Item).filter(models_items_in_stock.Item.id==item_id).first()
    item_to_update.name=item.name
    item_to_update.price=item.price
    item_to_update.description=item.description
    item_to_update.on_offer=item.on_offer
    item_to_update.in_stock=item.in_stock

    db.commit()

    return item_to_update

#To delete a particular item
@router.delete('/item/delete/{item_id}',tags=["For Manager"])
def delete_item(item_id:int):
    item_to_delete=db.query(models_items_in_stock.Item).filter(models_items_in_stock.Item.id==item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    db.delete(item_to_delete)
    db.commit()

    return item_to_delete

#To import items from a Excel Sheet
@router.post('/items/import/fromExcel', status_code=status.HTTP_201_CREATED,tags=["For Manager"])
async def import_items_from_excel(file: UploadFile = File(...)):
    # Reading the Excel file 
    df = pd.read_excel(file.file)
    
    items_data = df.to_dict('records')
   
    print(items_data) 
    #This is the Creation of items in the database
    items_created = []
    for item_data in items_data:
        print(item_data["name"])
       
        db_item = db.query(models_items_in_stock.Item).filter(models_items_in_stock.Item.name == item_data["name"]).first()
        if db_item is None:
            new_item = models_items_in_stock.Item(
                name=item_data["name"],
                price=item_data["price"],
                description=item_data["description"],
                on_offer=item_data["on_offer"],
                in_stock=item_data["in_stock"]
            )
            db.add(new_item)
            items_created.append(new_item)
    
    db.commit()
    
    return {'items_created': len(items_created)}

#For Employee 

#To update a specific item's stock
@router.put('/item/update/onlystock/{item_id}', response_model=Item, status_code=status.HTTP_200_OK,tags=["For Employee"])
def update_an_item_stock(item_id: int, quantity: int):
    item_to_update = db.query(models_items_in_stock.Item).filter(models_items_in_stock.Item.id == item_id).first()
    item_to_update.in_stock -= quantity

    db.commit()

    return item_to_update

#To create a sale report
@router.post('/sales/report/creation', status_code=status.HTTP_201_CREATED, tags=["For Employee"])
def submit_sale_report(customer: Customer, sales: List[Sales]):
    db_customer = models_customer_details.Customer(
        customer_name=customer.customer_name,
        phone_number=customer.phone_number,
    )
    db.add(db_customer)
    db.commit()

    for sale in sales:
        db_sale = models_sales_report.Sales(
            customer_id=db_customer.customer_id,
            item_id=sale.item_id,
            quantity=sale.quantity,
        )
        item_db = get_an_item_stock(sale.item_id)
    
        if item_db < sale.quantity:
            raise HTTPException(status_code=400,detail="Requested number of items are not in stock")
        else:
            db.add(db_sale)
            db.commit()
            update_an_item_stock(sale.item_id,sale.quantity)
        

    return {"message": "Sale report submitted successfully!"}

#To display customer details
@router.get('/customerDetails/getAll',response_model=List[Customer],status_code=200,tags=["For Employee"])
def get_all_customer_details():
    customer_details=db.query(models_customer_details.Customer).all()
    return customer_details

#To display sale details
@router.get('/SaleReport/getAll',response_model=List[Sales],status_code=200,tags=["For Employee"])
def get_all_sale_details():
    sale_details=db.query(models_sales_report.Sales).all()
    return sale_details