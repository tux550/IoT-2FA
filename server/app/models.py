from sqlalchemy import Column, Integer, String, Float

from sqlalchemy.dialects.postgresql import ARRAY

from database import Base 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    face_encoding = Column(ARRAY(Float))
    money = Column(Float, default=0.0)

metadata = Base.metadata

# if __name__ == '__main__':
#     db = SessionLocal()
#     for user in db.query(User).all():
#         print(user)