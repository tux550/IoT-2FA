from fastapi import FastAPI, Depends
import random

import database
import models
import schemas
from sqlalchemy.orm import Session

import numpy as np


app = FastAPI()


@app.post("/user")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_item = models.User(
        name=user.name, face_encoding=user.face_encoding, money=user.money, pin=user.pin)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return user

@app.post("/verify-pin")
def verify_pin(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    result = db.query(models.User).filter(models.User.id == user.id).all()

    if len(result) == 0:
        return False

    user_result = result[0]

    return user.pin == user_result.pin




@app.get("/user")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@app.get("/user_search")
def search_user(face_encoding: list[float], db: Session = Depends(database.get_db)):
    threshold = 0.8
    # fc_enc = np.array(face_encoding)

    # target_vector = vector(face_encoding)
    # query = db.query(models.User).filter(vector(
    # models.User.face_encoding).distance(target_vector) > threshold)
    query = db.query(models.User)


    result = query.all()

    topResults = []
    face_encoding = np.array(face_encoding)
    face_encoding_norm = np.linalg.norm(face_encoding)
    


    for possible_user in result:
        possible_user_encoding = np.array(possible_user.face_encoding)
        
        
        sim = np.dot(face_encoding, possible_user_encoding)/(np.linalg.norm(possible_user_encoding)*face_encoding_norm)

        if sim > threshold:
            topResults.append((possible_user.id, sim))

    topResults.sort(key=lambda x: x[1], reverse=True)

    print(topResults)

    if(len(topResults) == 0):
        return None

    return topResults[0][0]
