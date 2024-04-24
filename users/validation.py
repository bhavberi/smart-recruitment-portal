from abc import ABC, abstractmethod
import re
from fastapi import HTTPException, status
import phonenumbers

from utils import get_user_by_email, get_user_by_username
from models.users import Role

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

class UsernameValidator(AbstractHandler):
    """
    UserNameValidator is a concrete handler that checks if the username is alphanumeric.
    """
    
    def handle_request(self, request):
        if bool(re.match("^[a-zA-Z0-9]*$", request['username'])) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username should only contain alphanumeric characters",
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        else:
            return True
    
class EmailValidator(AbstractHandler):
    """
    EmailValidator is a concrete handler that checks if the email is in the correct format.
    """
    
    def handle_request(self, request):
        if bool(re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", request['email'])) is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is in wrong format",
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        else:
            return True
    
class EmailDuplicateValidator(AbstractHandler):
    """
    EmailDuplicateValidator is a concrete handler that checks if the email already exists.
    """
    
    def handle_request(self, request):
        if get_user_by_email(request['email']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        else:
            return True
    
class UsernameDuplicateValidator(AbstractHandler):
    """
    UsernameDuplicateValidator is a concrete handler that checks if the username already exists.
    """
    
    def handle_request(self, request):
        if get_user_by_username(request['username']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists",
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        else:
            return True
    
class PhoneNumberValidator(AbstractHandler):
    """
    PhoneNumberValidator is a concrete handler that checks if the phone number is valid.
    """
    
    def handle_request(self, request):
        try:
            contact = phonenumbers.parse(request['contact'], "IN")
            if not phonenumbers.is_valid_number(contact):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number"
                )
        except phonenumbers.phonenumberutil.NumberParseException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An Error Occured!",
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        else:
            return True

class RoleValidator(AbstractHandler):
    """
    RoleValidator is a concrete handler that checks if the role is valid.
    """
    
    def handle_request(self, request):
        if request['role'] not in Role.__members__:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Role"
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        else:
            return True
        
class PasswordValidator(AbstractHandler):
    """
    PasswordValidator is a concrete handler that checks if the password is strong.
    """
    
    def handle_request(self, request):
        if len(request['password']) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password should be atleast 8 characters long",
            )
        if self._next_handler is not None:
            return self._next_handler.handle_request(request)
        else:
            return True
