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
    create_application,
    get_user_application,
    approve_application,
    get_all_applications,
    get_all_listings,
    get_user,
    get_ai_response,
    get_user_details,
)

from validation import (
    AdminValidator,
    ListingValidator,
    SelfUserValidator,
    CandidateValidator,
    ExistingListingValidator,
    ExistingApplicationValidator,
    TwitterLinkValidator,
    LinkedinLinkValidator,
    RecruiterValidator,
    NoApplicationValidator
)

from build_report import ReportDirector, FullReportBuilder

router = APIRouter()


# make listing
@router.post(
    "/make_listing", status_code=status.HTTP_201_CREATED, response_model=ListingResponse
)
async def make_listing(
    listing: Listing,
    user=Depends(get_user),
):
    
    handler = AdminValidator()
    handler.escalate_request(ListingValidator())
    request = {"listing": listing.name, "role": user["role"]}
    handler.handle_request(request)

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

    handler = SelfUserValidator()
    handler.escalate_request(CandidateValidator()).escalate_request(ExistingListingValidator()).escalate_request(NoApplicationValidator()).escalate_request(TwitterLinkValidator()).escalate_request(LinkedinLinkValidator())
    request = {"user": application.user,
               "current_user": user["username"],
               "role": user["role"],
               "listing": application.listing,
               "twitter": application.twitter_id,
               "linkedin": application.linkedin_id}
    handler.handle_request(request)

    # create application
    create_application(application.model_dump())

    return {"user": application.user}


# get all the applications for a particular listing
@router.post("/get_applications", status_code=status.HTTP_200_OK, response_model=Applications)
async def get_applications(
    listing: Listing,
    user=Depends(get_user),
):
    
    handler = RecruiterValidator()
    handler.escalate_request(ExistingListingValidator())
    request = {"listing": listing.name, "role": user["role"]}
    handler.handle_request(request)

    return Applications(applications = get_all_applications(listing.name))


# get the report for an application
@router.post("/get_report", status_code=status.HTTP_200_OK, response_model=Report)
async def get_report(
    userapplication: UserApplication,
    user=Depends(get_user),
):

    handler = RecruiterValidator()
    handler.escalate_request(ExistingApplicationValidator())
    request = {"user": userapplication.username, "listing": userapplication.listing, "role": user["role"]}
    handler.handle_request(request)

    url = "/api/AI/llama"
    llama = get_ai_response(url)

    url = "/api/AI/mbti"
    mbti = get_ai_response(url)

    url = "/api/AI/report_gen"
    report_gen = get_ai_response(url)

    url = "/api/AI/sentiment"
    sentiment = get_ai_response(url)

    report_director = ReportDirector()
    report_director.builder = FullReportBuilder()
    return report_director.build_full_report(
        userapplication.username, llama, mbti, report_gen, sentiment
    )

# approve the application
@router.put("/approve", status_code=status.HTTP_202_ACCEPTED)
async def approve(
    userapplication: UserApplication,
    user=Depends(get_user),
):

    handler = RecruiterValidator()
    handler.escalate_request(ExistingApplicationValidator())
    request = {"user": userapplication.username, "listing": userapplication.listing, "role": user["role"]}
    handler.handle_request(request)

    application = get_user_application(
        userapplication.username, userapplication.listing
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
    
    handler = CandidateValidator()
    handler.escalate_request(SelfUserValidator()).escalate_request(ExistingApplicationValidator())
    request = {"user": userapplication.username, "listing": userapplication.listing, "role": user["role"], "current_user": user["username"]}
    handler.handle_request(request)

    application = get_user_application(
        userapplication.username, userapplication.listing
    )

    return {"status": application["accepted"]}
