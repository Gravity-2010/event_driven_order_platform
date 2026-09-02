from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/payments")
def create_payment(payload: dict):
    return {"payment": "successful", "order_id": payload["order_id"]}