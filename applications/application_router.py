from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
import requests

from models.applications import Listing, Report
from models.applications_otypes import (
    ListingResponse,
    ApplicationResponse,
    UserApplication,
    Approval,
    Applications,
    ApplicationInput,
    Listings,
)
from utils import (
    create_listing,
    validate_role_admin,
    validate_role_candidate,
    validate_twitter,
    validate_linkedin,
    create_application,
    validate_role_recruiter,
    get_user_application,
    approve_application,
    validate_user_application,
    validate_listing,
    get_all_applications,
    validate_user_and_application_user,
    get_all_listings,
    get_user,
    get_user_details,
)

router = APIRouter()


# make listing
@router.post(
    "/make_listing", status_code=status.HTTP_201_CREATED, response_model=ListingResponse
)
async def make_listing(
    listing: Listing,
    user=Depends(get_user),
):

    # check if user is admin
    if not validate_role_admin(user["role"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )

    # check if listing already exists
    if validate_listing(listing.name):
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
async def get_listings(
    user=Depends(get_user),
):

    return Listings(listings = get_all_listings())


# apply for job
@router.post("/apply", status_code=status.HTTP_201_CREATED, response_model=ApplicationResponse)
async def apply(
    application: ApplicationInput,
    user=Depends(get_user),
):

    # check if the logged in user is applying for himself
    if application.user != user["username"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Username",
            headers={"set-cookie": ""},
        )

    # check if the user is candidate
    if not validate_role_candidate(user["role"]):
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
    if not validate_user_application(application.user, application.listing):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already exists",
            headers={"set-cookie": ""},
        )

    # validate if the twitter and the linkedin links are correct
    if not validate_twitter(application.twitter_id) or not validate_linkedin(
        application.linkedin_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong social Media handles",
            headers={"set-cookie": ""},
        )

    # create application
    create_application(application.model_dump())

    return {"user": application.user}


# get all the applications for a particular listing
@router.post("/get_applications", status_code=status.HTTP_200_OK, response_model=Applications)
async def get_applications(
    listing: Listing,
    user=Depends(get_user),
):

    # validate if the user is recruiter
    if not validate_role_recruiter(user["role"]):
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

    return Applications(applications = get_all_applications(listing.name))


# get the report for an application
@router.post("/get_report", status_code=status.HTTP_200_OK, response_model=Report)
async def get_report(
    userapplication: UserApplication,
    user=Depends(get_user),
):

    # validate if the user is recruiter
    if not validate_role_recruiter(user["role"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )

    # validate if the application exists
    application = get_user_application(
        userapplication.username, userapplication.listing
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such application",
            headers={"set-cookie": ""},
        )

    report = Report()  # can use builder pattern here. For building the report

    report.user = userapplication.username

    url = "/api/AI/llama"
    response = requests.get(url)
    if response.status_code == 200:
        report.llama = response.text
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI didn't respond",
            headers={"set-cookie": ""},
        )

    url = "/api/AI/mbti"
    response = requests.get(url)
    if response.status_code == 200:
        report.mbti = response.text
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI didn't respond",
            headers={"set-cookie": ""},
        )

    url = "/api/AI/report_gen"
    response = requests.get(url)
    if response.status_code == 200:
        report.report_gen = response.text
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AI didn't respond",
            headers={"set-cookie": ""},
        )

    url = "/api/AI/sentiment"
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
    user=Depends(get_user),
):

    # validate if the user is recruiter
    if not validate_role_recruiter(user["role"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )

    # validate if the application exists
    application = get_user_application(
        userapplication.username, userapplication.listing
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such application",
            headers={"set-cookie": ""},
        )

    if not application["accepted"] == True:

        result = approve_application(userapplication.username, userapplication.listing)

        if not result.modified_count:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user details!",
            )

    return {"message": "User application updated successfully!"}


# check if the application is approved
@router.post("/get_application_status", status_code=status.HTTP_200_OK, response_model=Approval)
def get_application_status(
    userapplication: UserApplication,
    user=Depends(get_user),
):

    # valuidate if the user is a candidate
    if not validate_role_candidate(user["role"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No Permission",
            headers={"set-cookie": ""},
        )

    # validate if the user os checking his own application status
    if not validate_user_and_application_user(userapplication.username, user["username"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't check for other users",
            headers={"set-cookie": ""},
        )

    # validate if the application exists
    application = get_user_application(
        userapplication.username, userapplication.listing
    )

    if not application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such application",
            headers={"set-cookie": ""},
        )

    return {"status": application["accepted"]}
