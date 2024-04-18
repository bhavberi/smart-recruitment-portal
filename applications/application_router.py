from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
import requests

from models.applications import Listing, Report
from models.applications_otypes import ListingResponse, ApplicationResponse, UserApplication, Approval, Applications, ApplicationInput, Listings
from utils import (
    create_listing,
    validate_role_admin,
    validate_role_candidate,
    validate_twitter,
    validate_linkedin,
    create_application,
    validate_role_recruiter,
    validate_user,
    get_user_application,
    approve_application,
    validate_user_application,
    validate_listing,
    get_all_applications,
    validate_listing_name,
    validate_user_and_application_user,
    get_all_listings,
    get_user,
)

router = APIRouter()


# make listing
@router.post("/make_listing", status_code=status.HTTP_201_CREATED, response_model=ListingResponse)
async def make_listing(
    request: Request,
    listing: Listing,
):
    
    user = get_user(request)
    print("===============================")
    print(user)
    print("===============================")
    
    # check if user is admin
    if not validate_role_admin(user.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )
    
    # check if listing already exists
    if validate_listing_name(listing.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Listing already exists",
            headers={"set-cookie": ""},
        )
    
    # create listing
    create_listing(listing.model_dump())

    return {"name": listing.name}



# Get all the listings
@router.get("/get_Listings", status_code=status.HTTP_200_OK, response_model=Listings)
async def get_listings():
    
    # check if user if logged in
    url = '/api/users/details'
    response = requests.get(url)
    if response.status_code == 200:
        user = response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not logged in",
            headers={"set-cookie": ""},
        )
    
    # validate if the user is applicant or recruiter
    if not (validate_role_recruiter(user.role) or validate_role_candidate(user.role)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )
    
    listings = Listings()
    listings.listings = get_all_listings()
    return listings   # validate if correct



# apply for job
@router.post("/apply", status_code=status.HTTP_201_CREATED, response_model= ApplicationResponse)
async def apply(
    application: ApplicationInput,
):
    
    # check if user if logged in
    url = '/api/users/details'
    response = requests.get(url)
    if response.status_code == 200:
        user = response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not logged in",
            headers={"set-cookie": ""},
        )
    
    # check if the logged in user is applying for himself
    if application.user != user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Username",
            headers={"set-cookie": ""},
        )
    
    # check if the user is candidate
    if not validate_role_candidate(user.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )
    
    # validate if such a listing exists
    if not validate_listing(application.listing):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such listing",
            headers={"set-cookie": ""},
        )
    
    # validae if the application already exists
    if validate_user_application(application.user, application.listing):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already exists",
            headers={"set-cookie": ""},
        )
    
    # validate if the twitter and the linkedin links are correct
    if not validate_twitter(application.twitter_id) or not validate_linkedin(application.linkedin_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong social Media handles",
            headers={"set-cookie": ""},
        )
    
    # create application
    create_application(application.model_dump())

    return {"user": application.user}



# get all the applications for a particular listing
@router.get("/get_applications", status_code=status.HTTP_200_OK, response_model=Applications)
async def get_applications(
    listing: Listing,
):
    
    # check if user if logged in
    url = '/api/users/details'
    response = requests.get(url)
    if response.status_code == 200:
        user = response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not logged in",
            headers={"set-cookie": ""},
        )
    
    # validate if the user is recruiter
    if not validate_role_recruiter(user.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )
    
    # validate if listing exists
    if not validate_listing(listing.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such listing",
            headers={"set-cookie": ""},
        )
    
    applications = Applications()
    applications.applications = get_all_applications(listing.name)
    return applications   # validate if correct



# get the report for an application
@router.get("/get_report", status_code=status.HTTP_200_OK, response_model=Report)
async def get_report(
    userapplication: UserApplication,
):
    
    # check if user if logged in
    url = '/api/users/details'
    response = requests.get(url)
    if response.status_code == 200:
        user = response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not logged in",
            headers={"set-cookie": ""},
        )
    
    # validate if the user is recruiter
    if not validate_role_recruiter(user.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )
    
    # validate if user exists
    if not validate_user(userapplication.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such user",
            headers={"set-cookie": ""},
        )
    
    # validate if the application exists
    application = get_user_application(userapplication.username, userapplication.listing)

    if not application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No application by this user",
            headers={"set-cookie": ""},
        )
    
    report = Report()    # can use builder pattern here. For building the report

    report.user = userapplication.username

    url = '/api/AI/llama'
    response = requests.get(url)
    if response.status_code == 200:
        report.llama = response.text
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI didn't respond",
            headers={"set-cookie": ""},
        )
    
    url = '/api/AI/mbti'
    response = requests.get(url)
    if response.status_code == 200:
        report.mbti = response.text
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI didn't respond",
            headers={"set-cookie": ""},
        )
    
    url = '/api/AI/report_gen'
    response = requests.get(url)
    if response.status_code == 200:
        report.report_gen = response.text
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI didn't respond",
            headers={"set-cookie": ""},
        )
    
    url = '/api/AI/sentiment'
    response = requests.get(url)
    if response.status_code == 200:
        report.sentiment = response.text
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI didn't respond",
            headers={"set-cookie": ""},
        )

    return report



# approve the application
@router.put("/approve", status_code=status.HTTP_202_ACCEPTED)
async def approve(
    userapplication: UserApplication,
):
    
    # check if user if logged in
    url = '/api/users/details'
    response = requests.get(url)
    if response.status_code == 200:
        user = response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not logged in",
            headers={"set-cookie": ""},
        )
    
    # validate if the user is recruiter
    if not validate_role_recruiter(user.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )
    
    # validate if user exists
    if not validate_user(userapplication.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such user",
            headers={"set-cookie": ""},
        )
    
    # validate if the application exists
    application = get_user_application(userapplication.username, userapplication.listing)

    if not application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No application by this user",
            headers={"set-cookie": ""},
        )
    
    result = approve_application(userapplication.username, userapplication.listing)
    if not result.modified_count:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user details!"
            )

    return {"message": "User application updated successfully!"}



# chec if the application is approved
@router.get("/get_application_status", status_code=status.HTTP_200_OK, response_model=Approval)
def get_application_status(
    userapplication: UserApplication,
):
    
    # check if user if logged in
    url = '/api/users/details'
    response = requests.get(url)
    if response.status_code == 200:
        user = response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not logged in",
            headers={"set-cookie": ""},
        )
    
    # valuidate if the user is a candidate
    if not validate_role_candidate(user.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )
    
    # validate if the user os checking his own application status
    if not validate_user_and_application_user(userapplication.username, user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't check for other users",
            headers={"set-cookie": ""},
        )
    
    # validate if the application exists
    application = get_user_application(userapplication.username, userapplication.listing)

    if not application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such application",
            headers={"set-cookie": ""},
        )
    
    return {"status": application.accepted}