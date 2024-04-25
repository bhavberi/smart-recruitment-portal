from fastapi import HTTPException, Cookie, status
import re
import requests

from models.applications_otypes import ApplicationInput
from db import db

def create_listing(listing: dict):
    result = db.listings.insert_one(listing)
    return str(result.inserted_id)

def remove_listing(name: str):
    db.applications.delete_many({"listing": name})
    result = db.listings.delete_one({"name": name})
    return result

def get_all_listings():
    listings = db.listings.find()
    return listings


def get_user(access_token_se_p3: str = Cookie(None)):
    url = "http://users/current"
    response = requests.get(url, cookies={"access_token_se_p3": access_token_se_p3})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not logged in",
        )


def get_user_details(access_token_se_p3: str = Cookie(None)):
    url = "http://users/details"
    response = requests.get(url, cookies={"access_token_se_p3": access_token_se_p3})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not logged in",
        )