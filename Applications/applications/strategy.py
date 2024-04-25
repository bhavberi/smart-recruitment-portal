from fastapi import APIRouter, HTTPException, Depends, status
import requests
from os import getenv

from models.applications import Report, Listing
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
    approve_application,
    get_all_applications,
    get_all_user_applications,
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


class Context:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def execute_strategy(self):
        return self._strategy.execute()


class Strategy:
    def execute(self):
        pass


class Recruiter_listing(Strategy):
    def execute(listing: Listing,
                user):
        handler = RecruiterValidator()
        handler.escalate_request(ExistingListingValidator())
        request = {"listing": listing.name, "role": user["role"]}
        handler.handle_request(request)
        return Applications(applications=get_all_applications(listing.name))


class Candidate_listing(Strategy):
    def execute(listing: Listing,
                user):
        handler = CandidateValidator()
        handler.escalate_request(ExistingListingValidator())
        request = {"listing": listing.name, "role": user["role"]}
        handler.handle_request(request)
        return Applications(applications=get_all_user_applications(listing.name))