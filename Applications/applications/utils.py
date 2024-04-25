from fastapi import HTTPException, Cookie, status
import requests

from models.applications import Application
from db import db

def delete_applications(name: str):
    result = db.applications.delete_many({"listing": name})
    return result


def create_application(application: dict):
    # application["accepted"] = False
    application_built = Application(**application)
    result = db.applications.insert_one(application_built)
    return str(result.inserted_id)


def get_user_application(username: str, listing: str):
    application = db.applications.find_one({"user": username, "listing": listing})
    return application


def get_all_applications(name: str):
    applications = db.applications.find({"listing": name})
    return applications

def approve_application(username: str, listing: str):
    result = db.applications.update_one(
        {"user": username, "listing": listing}, {"$set": {"accepted": True}}
    )
    return result


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
    
def get_reply(url: str, payload):
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request Failed with status code: " + str(response.status_code),
        )