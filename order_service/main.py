from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from order_service.database import SessionLocal
from order_service.models_db import OrderDB
import httpx

app = FastAPI()

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    customer_id: int
    items: list[OrderItem]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/orders", status_code = 201)
def create_order(order: Order, db: Session = Depends(get_db)):
    db_order = OrderDB(customer_id = order.customer_id, items = [item.model_dump() for item in order.items])
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    try:
        payment_response = httpx.post('http://127.0.0.1:8001/payments', json = {"order_id": db_order.id}, timeout=3.0)
        payment_result = payment_response.json()
    except httpx.RequestError:
        payment_result = {"payment": "payment_service_unavailable"}
    return {"order_id": db_order.id, "customer_id": db_order.customer_id, "payment": payment_result["payment"]}

@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(OrderDB).filter(OrderDB.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": db_order.id, "customer_id": db_order.customer_id, "items": db_order.items}
