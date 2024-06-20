from typing import List
from pydantic import BaseModel


class User(BaseModel):
    name: str
    face_encoding: List[float]
    money: float
    
class UserCreate(User):
    pass  
