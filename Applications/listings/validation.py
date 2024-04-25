from abc import ABC, abstractmethod
from fastapi import HTTPException, status

from db import db

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

class ListingValidator(AbstractHandler):
    """
    The Concrete Handler for listing validation
    """

    def validate_listing(self, name: str):
        listing = db.listings.find_one({"name": name})
        if listing:
            return True
        else:
            return False
    
    def handle_request(self, request):
        if self.validate_listing(request["listing"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Listing already exists",
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
        listing = db.listings.find_one({"name": name})
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