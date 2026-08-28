from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    customer_id: int
    items: list[OrderItem]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/orders")
def create_order(order: Order):
    return {"Order Created for Customer Id": order.customer_id}