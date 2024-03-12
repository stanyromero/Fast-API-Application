from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import models_items_in_stock,models_sales_report,models_customer_details
from db.database import engine
from routers import items

app = FastAPI()

app.include_router(items.router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with the appropriate origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models_items_in_stock.Base.metadata.create_all(engine)
models_sales_report.Base.metadata.create_all(engine)
models_customer_details.Base.metadata.create_all(engine)
