from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import json
import face_recognition

import random

import database
import models
import schemas
from sqlalchemy.orm import Session

import numpy as np


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*',],
    allow_credentials=False,
    allow_methods=["*",],
    allow_headers=["*",],
)

TICKET_COST = 5

@app.post("/user")
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_item = models.User(
        name=user.name, face_encoding=user.face_encoding, money=user.money, pin=user.pin)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

@app.post("/verify-pin")
def verify_pin(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    result = db.query(models.User).filter(models.User.id == user.id).all()

    if len(result) == 0:
        return False

    user_result = result[0]

    VALID_PIN = user.pin == user_result.pin

    ENOUGH_MONEY = user_result.money - TICKET_COST >= 0

    BOUGHT_TICKET = VALID_PIN and ENOUGH_MONEY

    trans_item = models.Payment(
        user_id=user.id, user_name=user_result.name, amount=TICKET_COST, success=BOUGHT_TICKET
    )
    db.add(trans_item)

    if BOUGHT_TICKET:
        user_result.money -= TICKET_COST
        db.add(user_result)
    
    db.commit()
    db.refresh(user_result)

    return BOUGHT_TICKET


@app.get("/payment")
def read_payments(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    payments = db.query(models.Payment).order_by(models.Payment.date).offset(skip).limit(limit).all()

    return payments


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

    topResults : list[tuple[int, float]] = []
    face_encoding = np.array(face_encoding)
    face_encoding_norm = np.linalg.norm(face_encoding)
    


    for possible_user in result:
        user_encodings = json.loads(possible_user.face_encoding)
        for encoding in  user_encodings:
        # print(len(user_encodings))
        # print(type(user_encodings[0]))
            possible_user_encoding = np.array(encoding)
            
            
            # sim : float = np.dot(face_encoding, possible_user_encoding)/(np.linalg.norm(possible_user_encoding)*face_encoding_norm)

            sim: float = face_recognition.face_distance([face_encoding], possible_user_encoding)[0]


            # if sim > threshold:
            possible_user_id: int = possible_user.id
            tupleData = (possible_user_id, sim)
            topResults.append(tupleData)


    if(len(topResults) == 0):
        return None


    k = 5 
    topResults.sort(key=lambda x: x[1], reverse=False)
    topResults = topResults[:k]

    print(topResults)

    resultsDir = {
        x[0] : [] for x in topResults
    }
    for r in topResults:
        resultsDir[r[0]].append(r[1])
    
    keyLenDict = {key: len(value) for key, value in resultsDir.items()}

    maxLen = max(keyLenDict.values())

    candidates = {}

    for key in keyLenDict:
        if keyLenDict[key] == maxLen:
            candidates[key] = min(resultsDir[key])
    
    # candidate with max similarity
    bestMatch = min(candidates, key=candidates.get)
    
    print(resultsDir)
    print(keyLenDict)
    print(candidates)
    print(bestMatch)

    return bestMatch

    #return topResults[0][0]
