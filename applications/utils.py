from fastapi import HTTPException, Request, status, FastAPI
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
    pattern = r'^https?://twitter.com/[A-Za-z0-9_]{1,15}(?:/)?$'
    return bool(re.match(pattern, id))

def validate_linkedin(id: str):
    pattern = r'^https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?$'
    return bool(re.match(pattern, id))

def validate_user(username: str):   # implement
    return True

def validate_user_and_application_user(username_application: str, username: str):
    return username == username_application

def validate_listing(name: str):
    listing = db.listings.find_one({"name": name})
    if listing:
        return True
    else:
        return False

def validate_listing_name(name: str):
    listing = db.listings.find_one({"name": name})
    if listing:
        return False
    else:
        return True

def validate_user_application(username: str, listingname: str):
    application = db.applications.find_one({"user": username, "listing": listingname})
    if application:
        return False
    return True

def create_listing(listing: dict):
    result = db.listings.insert_one(listing)
    return str(result.inserted_id)

def create_application(application: ApplicationInput):
    application["approved"] = False
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
    result = db.applications.update_one({"username": username, "listing": listing}, {
                        "$set": {"accepted": True}})
    return result

def get_user(request: Request):
    username = request.session.get('username')
    session = requests.Session()
    session.headers['username'] = username

    print("here")
    url = 'http://users/details'
    response = session.get(url)
    print(response)
    if response.status_code == 200:
        print("got_here")
        return response.json()
    else:
        raise HTTPException(
            status_code=400,
            detail="Not logged in",
            headers={"set-cookie": ""},
        )
    
# app = FastAPI()
# @app.get('/get_firstuser')
# def get_user():
#     api_url = "http://localhost/api/users/details"
#     user = requests.get(api_url).json()
#     return user