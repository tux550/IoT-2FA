from fastapi import FastAPI
from . import models, schemas, database 
from sqlalchemy import Session 

import numpy as np 


app = FastAPI()


@app.post("/users/")
def create_user(user: schemas.UserCreate):
    db= database.get_db()    
    
    db_item = models.User(name=user.name, encoding=user.encoding, money=user.money)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return user


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10):
    db = database.get_db()
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/user_search/")
def search_user(face_encoding: list[float]):
    threshold =  0.85
    db= database.get_db()
    #fc_enc = np.array(face_encoding)
    
    target_vector =  func.vector(face_encoding)
    query = db.query(models.User).filter(func.vector(models.User.face_encoding).distance(target_vector) > threshold)
    
    result = query.first()
    
    return result
    
    
    
    
    