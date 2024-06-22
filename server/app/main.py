from fastapi import FastAPI, Depends
import random

import database
import models
import schemas
from sqlalchemy.orm import Session

import numpy as np


app = FastAPI()


@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_item = models.User(
        name=user.name, face_encoding=user.face_encoding, money=user.money)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return user


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@app.get("/user_search/")
def search_user(face_encoding: list[float], db: Session = Depends(database.get_db)):
    # threshold = 0.85
    # fc_enc = np.array(face_encoding)

    # target_vector = vector(face_encoding)
    # query = db.query(models.User).filter(vector(
    # models.User.face_encoding).distance(target_vector) > threshold)

    query = db.query(models.User)

    result = query.first()

    user_exists = random.randint(0, 1)

    print('user exists', user_exists)

    if (user_exists == 0):
        return None
    else:
        return result
