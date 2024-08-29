from pydantic import BaseModel
from datetime import datetime

class OrdersOut(BaseModel):
    OrderID: int
    OrderTitle: str
    OrderDescription: str
    CustomerID: int
    CreatedAt: datetime