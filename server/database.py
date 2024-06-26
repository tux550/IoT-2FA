
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
# FOR VECTOR COLUMN 
from sqlalchemy.dialects.postgresql import ARRAY


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@postgres/iot" #  "postgresql://user:password@postgresserver/db"
 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    face_encoding = Column(ARRAY(Float))
    money = Column(Float, default=0.0)
    