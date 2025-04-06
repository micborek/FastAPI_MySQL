from fastapi import FastAPI, HTTPException, Depends, status
from fastapi_pagination import Page, add_pagination, paginate
from database_handler import get_db
import uvicorn
import logging
import models
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from validators import OrdersOut

from constants import API_METADATA

# set up a logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# set up fast API app
app = FastAPI(**API_METADATA)
add_pagination(app)

db_session = Annotated[Session, Depends(get_db)]


# endpoints
@app.get("/", tags=["Root"])
async def index():
    """Return docs message for default server's address"""
    return {"message": "Go to http://127.0.0.1:8000/docs to check available endpoints."}


# users endpoints
@app.get("/users/{user_id}", tags=["Users"])
async def get_user(user_id: int, db: db_session):
    """Endpoint for getting user's data by its id"""

    user_to_get = db.query(models.User).filter(models.User.UserID == user_id).first()
    if not user_to_get:
        raise HTTPException(status_code=404, detail=f"User does not exist")
    return user_to_get


@app.post("/users/", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def add_user(first_name: str, last_name: str, email: str, db: db_session):
    """Endpoint for adding a new user. Return created UserID or return an exception"""

    user = models.User(FirstName=first_name, LastName=last_name, Email=email)
    db.add(user)
    db.commit()

    return {"UserID": user.UserID}


@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int, db: db_session):
    """POST endpoint for deleting an existing user."""

    user_to_delete = db.query(models.User).filter(models.User.UserID == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail=f"User does not exist")
    db.delete(user_to_delete)
    db.commit()

    return {"UserID": user_to_delete.UserID}


# orders endpoints
@app.get("/orders/{order_id}", tags=["Orders"])
async def get_order(order_id: int, db: db_session):
    """Endpoint for getting order's data"""
    order_to_get = db.execute(
        select(models.Order).order_by(models.Order.OrderID == order_id)
    ).first()
    if not order_to_get:
        raise HTTPException(status_code=404, detail="Order does not exist")
    return order_to_get


@app.get("/orders/{user_id}", tags=["Orders"])
async def get_orders_by_user(user_id: int, db: db_session) -> Page[OrdersOut]:
    """Endpoint for getting user's orders. Pagination is supported"""
    orders_to_get = db.query(models.Order).filter(models.Order.UserID == user_id).all()
    if not orders_to_get:
        raise HTTPException(
            status_code=404, detail="No orders found for the requested user"
        )
    return paginate(orders_to_get)


@app.post("/orders/", status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def add_order(
    order_title: str, order_description: str, user_id: int, db: db_session
):
    """Endpoint for adding a new order. Return 400 status code if there occurs primary-foreign key integrity exception"""
    try:
        order = models.Order(
            OrderTitle=order_title,
            OrderDescription=order_description,
            CustomerID=user_id,
        )
        db.add(order)
        db.commit()

        return {"OrderID": order.OrderID}
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Cannot add or update a child row. Check if entered CustomerID exists",
        )


# TODO: ADD UPDATE order
# TODO: ADD DELETE ORDER

# TODO: ADD AUTHENTICATION

# run in debug mode in pycharm
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# reload stuck python process for uvicorn reload example
# tasklist /FI "IMAGENAME eq python.exe"
# taskkill /PID 15332  /F
