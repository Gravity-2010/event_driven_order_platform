from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

order_dict = {}
next_order_id = 1

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
    global next_order_id 
    order_dict[next_order_id] = order
    next_order_id += 1
    return {"Order Created for Customer Id": order.customer_id}

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id not in order_dict:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_dict[order_id]