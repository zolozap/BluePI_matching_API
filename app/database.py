import os
import pymongo
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


class Cards(BaseModel):
    new_game: bool
    click_a: int
    click_b: int


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

def create_or_update_cards(current_user,cards_index_a,cards_index_b,click_counter,your_best_score):
    # print("DB INPUT",current_user,cards_index_a,cards_index_b,click_counter)
    db = get_db()
    now = datetime.now()
    if your_best_score > 0:
        your_best_score = your_best_score
    else:
        your_best_score = 0
    objs = {'username':current_user,'cards_index_a':cards_index_a,'cards_index_b':cards_index_b,'matches_values':[],'click_counter':click_counter,'best_click_counter':your_best_score,'created_date':now,'updated_date':now}
    result = db.cards.find_one_and_update({'username':current_user},{'$set':objs},upsert=True,return_document=ReturnDocument.AFTER)
    result.pop('_id',None)
    return result

def get_data_cards(current_user):
    db = get_db()
    result = db.cards.find_one({'username':current_user},{'_id':0})
    return result

def update_click_counter(current_user,click_counter,best_score):
    db = get_db()
    # Global best
    global_best = list(db.cards.find({'best_click_counter':{'$gt':0}},{'_id':0,'best_click_counter':1}).sort('best_click_counter', pymongo.ASCENDING))
    # print(global_best)
    if best_score is True:
        result = db.cards.find_one_and_update({'username':current_user},{'$set':{'click_counter':click_counter,'best_click_counter':click_counter}},projection={'_id':0,'click_counter':1,'best_click_counter':1},upsert=True,return_document=ReturnDocument.AFTER)
    else:
        result = db.cards.find_one_and_update({'username':current_user},{'$set':{'click_counter':click_counter}},projection={'_id':0,'click_counter':1,'best_click_counter':1},upsert=True,return_document=ReturnDocument.AFTER)
    # print(type(result),result)
    result['global_best_score'] = [gb['best_click_counter'] for gb in global_best][0]
    return result

def get_or_update_matching(current_user,matches_array,matches_values):
    db = get_db()
    now = datetime.now()
    get_matches_array = db.cards.find_one({'username':current_user},{'_id':0,'matches_values':1,'click_counter':1,'best_click_counter':1})
    if matches_values:
        obj_matches_values = {'cards_values':str(matches_values),'cards_index':matches_array}
        result = db.cards.find_one_and_update({'username':current_user},{'$set':{'updated_date':now},'$addToSet':{'matches_values':obj_matches_values}},projection={'_id':0,'matches_values':1,'click_counter':1,'best_click_counter':1},upsert=True,return_document=ReturnDocument.AFTER)
    else:
        result = get_matches_array
    return result


def get_global_score(current_user):
    db = get_db()
    result = {}
    # Global best
    global_best = list(db.cards.find({'best_click_counter':{'$gt':0}},{'_id':0,'best_click_counter':1}).sort('best_click_counter', pymongo.ASCENDING))
    result['global_best_score'] = [gb['best_click_counter'] for gb in global_best][0]
    # Get your best score for new game
    get_your_best = db.cards.find_one({'username':current_user},{'_id':0,'best_click_counter':1})
    result['your_best_score'] = get_your_best['best_click_counter']
    return result