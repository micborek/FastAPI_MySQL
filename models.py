from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database_handler import (
    Base,
    engine
)
from sqlalchemy.sql import func


class User(Base):
    """Object–relational mapping """
    __tablename__ = 'users'

    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Email = Column(String(100), nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())


class Order(Base):
    """Object–relational mapping """
    __tablename__ = 'orders'

    OrderID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    OrderTitle = Column(String(100), nullable=False)
    OrderDescription = Column(String(200))
    UserID = Column(ForeignKey(User.UserID))
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now())


# Create all tables stored in this metadata if non-existent
Base.metadata.create_all(engine)
