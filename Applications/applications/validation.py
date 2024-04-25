from abc import ABC, abstractmethod
from fastapi import HTTPException, status
import re
from os import getenv

from db import db
from utils import get_user_application, get_reply

INTER_COMMUNICATION_SECRET = getenv("INTER_COMMUNICATION_SECRET", "inter-communication-secret")

class AbstractHandler(ABC):
    """
    The Handler interface declares a method for building the chain of handlers.
    """
    
    _next_handler = None

    @abstractmethod
    def handle_request(self, request):
        pass

    def escalate_request(self, nextHandler):
        self._next_handler = nextHandler
        return self._next_handler

class AdminValidator(AbstractHandler):
    """
    The Concrete Handler for admin validation
    """

    def validate_role_admin(self, role: str):
        if role != "admin":
            return False
        return True
    
    def handle_request(self, request):
        if not self.validate_role_admin(request["role"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not An Admin",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True

class SelfUserValidator(AbstractHandler):
    """
    The Concrete Handler for checking whether the user is himself
    """
    
    def handle_request(self, request):
        if request["user"] != request["current_user"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect Username",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True

class CandidateValidator(AbstractHandler):
    """
    The Concrete Handler for checking whether the user is a candidate
    """
    
    def validate_role_candidate(self, role: str):
        if role != "candidate":
            return False
        return True
    
    def handle_request(self, request):
        if not self.validate_role_candidate(request["role"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Permission",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True
    
class ExistingListingValidator(AbstractHandler):
    """
    The Concrete Handler for checking whether the listing exists
    """

    def validate_listing(self, name: str):
        payload = {
            "listing": name,
            "secret": INTER_COMMUNICATION_SECRET
        }
        listing = get_reply(f"http://listings/get_listing", payload)
        if listing:
            return True
        else:
            return False
    
    def handle_request(self, request):
        if not self.validate_listing(request["listing"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No such listing",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True

class NoApplicationValidator(AbstractHandler):
    """
    The Concrete Handler for checking whether the application exists
    """

    def validate_user_application(self, username: str, listingname: str):
        application = get_user_application(username, listingname)
        if application:
            print("Application Found")
            return False
        return True
    
    def handle_request(self, request):
        if not self.validate_user_application(request["user"], request["listing"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Application already exists",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True

class TwitterLinkValidator(AbstractHandler):
    """
    The Concrete Handler for checking whether the twitter link is valid
    """

    def validate_twitter(self, id: str):
        pattern = r"^https?://twitter.com/[A-Za-z0-9_]{1,15}(?:/)?$"
        return bool(re.match(pattern, id))
    
    def handle_request(self, request):
        if not self.validate_twitter(request["twitter"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Twitter Link",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True

class LinkedinLinkValidator(AbstractHandler):
    """
    The Concrete Handler for checking whether the linkedin link is valid
    """

    def validate_linkedin(self, id: str):
        pattern = r"^https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+/?$"
        return bool(re.match(pattern, id))
    
    def handle_request(self, request):
        if not self.validate_linkedin(request["linkedin"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Linkedin Link",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True

class RecruiterValidator(AbstractHandler):
    """
    The Concrete Handler for checking whether the user is a recruiter
    """

    def validate_role_recruiter(self, role: str):
        if role != "recruiter":
            return False
        return True
    
    def handle_request(self, request):
        if not self.validate_role_recruiter(request["role"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Permission",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True

class ExistingApplicationValidator(AbstractHandler):
    """
    The Concrete Handler for checking whether the application exists
    """

    def validate_user_application(self, username: str, listingname: str):
        application = get_user_application(username, listingname)
        if application:
            return True
        return False
    
    def handle_request(self, request):
        if not self.validate_user_application(request["user"], request["listing"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Application does not exist",
                headers={"set-cookie": ""},
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        return True