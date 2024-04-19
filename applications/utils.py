from fastapi import HTTPException, Cookie, status
import re
import requests

from models.applications_otypes import ApplicationInput
from db import db


def validate_role_admin(role: str):
    if role != "admin":
        return False
    return True


def validate_role_candidate(role: str):
    if role != "candidate":
        return False
    return True


def validate_role_recruiter(role: str):
    if role != "recruiter":
        return False
    return True


def validate_twitter(id: str):
    pattern = r"^https?://twitter.com/[A-Za-z0-9_]{1,15}(?:/)?$"
    return bool(re.match(pattern, id))


def validate_linkedin(id: str):
    pattern = r"^https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?$"
    return bool(re.match(pattern, id))


def validate_user_and_application_user(username_application: str, username: str):
    return username == username_application


def validate_listing(name: str):
    print(name)
    listing = db.listings.find_one({"name": name})
    print(listing)
    if listing:
        return True
    else:
        return False


def validate_user_application(username: str, listingname: str):
    application = db.applications.find_one({"user": username, "listing": listingname})
    if application:
        return False
    return True


def create_listing(listing: dict):
    result = db.listings.insert_one(listing)
    return str(result.inserted_id)


def create_application(application: ApplicationInput):
    application["accepted"] = False
    result = db.applications.insert_one(application)
    return str(result.inserted_id)


def get_user_application(username: str, listing: str):
    application = db.applications.find_one({"user": username, "listing": listing})
    return application


def get_all_applications(name: str):
    applications = db.applications.find({"listing": name})
    return applications


def get_all_listings():
    listings = db.listings.find()
    return listings


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
