from fastapi import APIRouter, HTTPException, Depends, status
from os import getenv

from models.applications import Report, Listing, Status
from models.applications_otypes import (
    ApplicationResponse,
    UserApplication,
    Approval,
    Applications,
    ApplicationInput,
)
from utils import (
    delete_applications,
    create_application,
    get_user_application,
    update_status_application,
    get_all_applications,
    get_user,
    get_reply,
)

from validation import (
    AdminValidator,
    SelfUserValidator,
    CandidateValidator,
    ExistingListingValidator,
    ExistingApplicationValidator,
    TwitterLinkValidator,
    LinkedinLinkValidator,
    RecruiterValidator,
    NoApplicationValidator
)

from strategy import Context, Recruiter_listing, Candidate_listing
from build_report import ReportDirector, FullReportBuilder

router = APIRouter()

INTER_COMMUNICATION_SECRET = getenv(
    "INTER_COMMUNICATION_SECRET", "inter-communication-secret")

# delete applications


@router.post("/remove_applications", status_code=status.HTTP_200_OK)
async def delete_listing(
    listing: str,
    user=Depends(get_user),
):
    print(listing)
    handler = AdminValidator()
    request = {"role": user["role"]}
    handler.handle_request(request)

    # delete applications from a listing
    delete_applications(listing)

    return {"name": listing}

# apply for job


@router.post("/apply", status_code=status.HTTP_201_CREATED, response_model=ApplicationResponse)
async def apply(
    application: ApplicationInput,
    user=Depends(get_user),
):

    handler = SelfUserValidator()
    handler.escalate_request(CandidateValidator()).escalate_request(ExistingListingValidator()).escalate_request(
        NoApplicationValidator()).escalate_request(TwitterLinkValidator()).escalate_request(LinkedinLinkValidator())
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
    if (user["role"] == "candidate"):
        context = Context(Candidate_listing())
        context.execute_strategy()
    elif (user["role"] == "recruiter"):
        context = Context(Recruiter_listing())
        context.execute_strategy()
    # handler = RecruiterValidator()
    # handler.escalate_request(ExistingListingValidator())
    # request = {"listing": listing.name, "role": user["role"]}
    # handler.handle_request(request)

    # return Applications(applications=get_all_applications(listing.name))

    # get the report for an application


@router.post("/get_report", status_code=status.HTTP_200_OK, response_model=Report)
async def get_report(
    userapplication: UserApplication,
    user=Depends(get_user),
):
    handler = RecruiterValidator()
    handler.escalate_request(ExistingApplicationValidator())
    request = {"user": userapplication.username,
               "listing": userapplication.listing, "role": user["role"]}
    handler.handle_request(request)

    application = get_user_application(
        userapplication.username, userapplication.listing
    )

    mbti = get_reply(f"http://mbti/{application['twitter_id'].split('/')[-1]}", {"secret": INTER_COMMUNICATION_SECRET})
    llama_input = mbti["personality"]
    llama = get_reply(f"http://llama/{llama_input}", {"secret": INTER_COMMUNICATION_SECRET})["result"]
    sentiment = get_reply(f"http://sentiment/{application['twitter_id'].split('/')[-1]}", {"secret": INTER_COMMUNICATION_SECRET})
    # skills = requests.get(f"http://localhost:8080/linkedin/{application['linkedin_id']}").text

    skills = "Damn good at coding!"

    report_director = ReportDirector()
    report_director.builder = FullReportBuilder()
    return report_director.build_full_report(
        userapplication.username, llama, mbti, sentiment, skills
    )

# approve the application


@router.put("/approve", status_code=status.HTTP_202_ACCEPTED)
async def approve(
    userapplication: UserApplication,
    user=Depends(get_user),
):

    handler = RecruiterValidator()
    handler.escalate_request(ExistingApplicationValidator())
    request = {"user": userapplication.username,
               "listing": userapplication.listing, "role": user["role"]}
    handler.handle_request(request)

    application = get_user_application(
        userapplication.username, userapplication.listing
    )

    if application["status"] == Status.pending:
        result = update_status_application(userapplication.username, userapplication.listing, Status.accepted)
        if not result.modified_count:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user details!",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already approved!",
        )

    return {"message": "User application updated successfully!"}

# reject the application
@router.put("/reject", status_code=status.HTTP_202_ACCEPTED)
async def reject(
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

    if application["status"] == Status.pending:
        result = update_status_application(userapplication.username, userapplication.listing, Status.rejected)
        if not result.modified_count:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user details!",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already approved!",
        )

    return {"message": "User application updated successfully!"}


# check if the application is approved
@router.post("/get_application_status", status_code=status.HTTP_200_OK, response_model=Approval)
def get_application_status(
    userapplication: UserApplication,
    user=Depends(get_user),
):

    handler = CandidateValidator()
    handler.escalate_request(SelfUserValidator()).escalate_request(
        ExistingApplicationValidator())
    request = {"user": userapplication.username, "listing": userapplication.listing,
               "role": user["role"], "current_user": user["username"]}
    handler.handle_request(request)

    application = get_user_application(
        userapplication.username, userapplication.listing
    )

    return {"status": application["status"]}
