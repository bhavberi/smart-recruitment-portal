from fastapi import HTTPException, Request, status, Cookie
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import EmailStr
from typing import Optional
from pytz import timezone
from os import getenv
import phonenumbers
import re

from models.users import User, Role
from db import db


# JWT Authentication
SECRET_KEY = getenv("JWT_SECRET_KEY", "this_is_my_very_secretive_secret") + "__d7__"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash password using bcrypt
def get_password_hash(password: str):
    return pwd_context.hash(password)


# Verify password using bcrypt
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Create User in MongoDB
def create_user(user: dict):
    user["password"] = get_password_hash(user["password"])
    result = db.users.insert_one(user)
    return str(result.inserted_id)


# Update User in MongoDB
def update_user(user: dict):
    user["password"] = get_password_hash(user["password"])
    result = db.users.replace_one({"username": user["username"]}, user)
    if not result.modified_count:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user details!",
        )
    return True


# Update user password in MongoDB
def update_user_password(username: str, password: str):
    hashed_password = get_password_hash(password)
    result = db.users.update_one(
        {"username": username}, {"$set": {"password": hashed_password}}
    )
    if not result.modified_count:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password!",
        )
    return True


# Get User from MongoDB by Username
def get_user_by_username(username: str):
    user = db.users.find_one({"username": username})
    if user:
        return User(**user)
    else:
        return None


# Get User from MongoDB by Email
def get_user_by_email(email: EmailStr):
    user = db.users.find_one({"email": email})
    if user:
        return User(**user)
    else:
        return None


# Authenticate User by Username and Password
def authenticate_user(username_email: str, password: str):
    if "@" in username_email:
        user = get_user_by_email(username_email)
    else:
        user = get_user_by_username(username_email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


# Create Access Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone("UTC")) + expires_delta
    else:
        expire = datetime.now(timezone("UTC")) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dependency for User Authentication
async def get_current_user(access_token_se_p3: str = Cookie(None)):
    if access_token_se_p3 is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    try:
        payload = jwt.decode(access_token_se_p3, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        user = get_user_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        del user.password
        return user
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


# Function to check the current user is logged in or not
async def check_current_user(access_token_se_p3: str = Cookie(None)):
    if access_token_se_p3 is None:
        return None
    try:
        payload = jwt.decode(access_token_se_p3, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        user = get_user_by_username(username)
        if user is None:
            return None
        del user.password
        return access_token_se_p3
    except JWTError:
        return None
