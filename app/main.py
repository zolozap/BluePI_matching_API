import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from .database import *
from .logic import *
from dotenv import load_dotenv
load_dotenv()

# openssl rand -hex 32
SECRET_KEY = os.environ.get('SECRETS_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define Origin * for test
origins = [
    "*",
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def create_new_users(users:User):
    results = create_users(users.dict())
    return {'results':results}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile/", response_model=User)
async def read_users_profile(current_user: User = Depends(get_current_active_user)):
    """
    **Get user profile**
    """
    return current_user


@app.post("/cards/",response_description="Cards parameter, Global best score, Your score")
async def matches_cards(click: Cards, current_user: User = Depends(get_current_active_user)):
    """
    **Start game cards matches**

    - **name_game**: status of start new game, data_type is boolean (true,false) Use **true** for **start new** and Use **false with click_a and click_b** when **game is running..**
    - **click_a**: array index users first click, data_type is integer (0 - 12)
    - **click_b**: array index users second click, data_type is integer (0 - 12)
    - Please see more detail in "Schema"
    """
    results = get_card(current_user.username,click)
    return results