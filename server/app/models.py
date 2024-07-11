from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime

from sqlalchemy.dialects.postgresql import ARRAY

from database import Base 
from sqlalchemy.sql import func  # Import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    face_encoding = Column(ARRAY(Float))
    money = Column(Float, default=0.0)
    pin = Column(String)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    user_name = Column(String)
    amount = Column(Float)
    date = Column(DateTime(timezone=True), default=func.now())
    success = Column(Boolean)

metadata = Base.metadata

# if __name__ == '__main__':
#     db = SessionLocal()
#     for user in db.query(User).all():
#         print(user)