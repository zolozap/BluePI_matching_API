import os
from pymongo import MongoClient,ReturnDocument
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
load_dotenv()

# openssl rand -hex 32
SECRET_KEY = os.environ.get('SECRETS_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    hashed_password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_db():
    client = MongoClient(os.environ.get('CONNECT_STRING'))
    db = client.bluepi_matching_cards
    return db

def create_users(payload):
    db = get_db()
    # print("On create :", payload)
    result = db.users.find_one_and_update({'username':payload['username'], 'email':payload['email']},{'$set':payload},upsert=True,return_document=ReturnDocument.AFTER)
    result.pop('_id',None)
    result.pop('hashed_password',None)
    return result

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str):
    db = get_db()
    has_username = db.users.find_one({"username":username},{'_id':0})
    # print(has_username)
    if has_username:
        user_dict = has_username
        return UserInDB(**user_dict)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    # print("authenticate_user:",user.hashed_password)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def records_score(score: int):
#     db = get_db()
#     db.score