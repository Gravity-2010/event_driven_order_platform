from order_service.database import Base, engine
from order_service.models_db import OrderDB

Base.metadata.create_all(bind=engine)