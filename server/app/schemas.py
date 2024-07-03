from typing import List
from pydantic import BaseModel


class User(BaseModel):
    name: str
    face_encoding: List[float]
    money: float
    pin: str
    
class UserCreate(User):
    pass  

class UserLogin(BaseModel):
    id: int
    pin: str