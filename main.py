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
# TODO: add PUT(for update); change customers to 'users'
@app.get("/", tags=["Root"])
async def index():
    """Default server's address"""
    return {"message": "Go to http://127.0.0.1:8000/docs to check available endpoints."}


@app.get("/users/{user_id}", tags=["Users"])
async def get_user(user_id: int, db: db_session):
    """GET Endpoint for getting user's data"""
    customer_to_get = (
        db.query(models.User).filter(models.User.UserID == user_id).first()
    )
    if not customer_to_get:
        raise HTTPException(status_code=404, detail=f"User does not exist")
    return customer_to_get


@app.get("/orders/{user_id}", tags=["Orders"])
async def get_orders_by_user(customer_id: int, db: db_session) -> Page[OrdersOut]:
    """GET Endpoint for getting customer's orders. Pagination is supported"""
    orders_to_get = (
        db.query(models.Order).filter(models.Order.UserID == customer_id).all()
    )
    if not orders_to_get:
        raise HTTPException(status_code=404, detail="Customer does not exist")
    return paginate(orders_to_get)


@app.post("/users/", status_code=status.HTTP_201_CREATED, tags=["Users"])
async def add_customer(
    customer_first_name: str, customer_last_name: str, email: str, db: db_session
):
    """POST endpoint for adding a new customer. Return created customers CustomerID or return an exception"""
    try:
        user = models.User(
            FirstName=customer_first_name, LastName=customer_last_name, Email=email
        )
        db.add(user)
        db.commit()

        return {"CustomerID": user.UserID}

    except Exception as e:
        logger.exception(
            f"An exception occurred when trying to insert to customers table: {e}"
        )


@app.delete("/users/{user_id}", tags=["Users"])
async def delete_user(user_id: int, db: db_session):
    """POST endpoint for deleting an existing user."""
    try:
        user_to_delete = (
            db.query(models.User).filter(models.User.UserID == user_id).first()
        )
        if not user_to_delete:
            raise HTTPException(status_code=404, detail=f"User does not exist")
        db.delete(user_to_delete)
        db.commit()

        return {"CustomerID": user_to_delete.UserID}

    except Exception as e:
        logger.exception(f"An exception occurred when trying to insert to customers table: {e}")
        raise HTTPException(status_code=500, detail='An exception occurred when trying to insert to customers table.')


# TODO: ADD UPDATE CUSTOMER


# ORDERS
@app.get("/orders/{order_id}", tags=["Orders"])
async def get_order(order_id: int, db: db_session):
    """GET Endpoint for getting order's data"""
    order_to_get = db.execute(
        select(models.Order).order_by(models.Order.OrderID == order_id)
    ).first()
    if not order_to_get:
        raise HTTPException(status_code=404, detail="Order does not exist")
    return order_to_get


@app.post("/orders/", status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def add_order(
    order_title: str, order_description: str, customer_id: int, db: db_session
):
    """POST Endpoint for adding a new order. Return 400 status code if there occurs primary-foreign key integrity exception"""
    try:
        order = models.Order(
            OrderTitle=order_title,
            OrderDescription=order_description,
            CustomerID=customer_id,
        )
        db.add(order)
        db.commit()

        return {"OrderID": order.OrderID}
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Cannot add or update a child row. Check if entered CustomerID exists",
        )
    except Exception as e:
        logger.exception(
            f"An exception occurred when trying to insert to orders table: {e}"
        )
        raise HTTPException(
            status_code=500,
            detail="An exception occurred when trying to insert to orders table.",
        )


# TODO: ADD DELETE ORDER
# TODO: ADD AUTHENTICATION

# run in debug mode in pycharm
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# reload stuck python process for uvicorn reload example
# tasklist /FI "IMAGENAME eq python.exe"
# taskkill /PID 15332  /F
