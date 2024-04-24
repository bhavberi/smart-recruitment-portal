from fastapi import APIRouter, HTTPException, Depends, Response, Request, status, Cookie
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import re

from models.users import User
from models.users_otypes import UserLoginResponse, ChangePasswordInput, UserEditInput
from utils import (
    create_access_token,
    check_current_user,
    get_current_user,
    get_user_by_email,
    get_user_by_username,
    create_user,
    authenticate_user,
    update_user,
    update_user_password,
)

from validation import (
    AbstractHandler,
    EmailValidator,
    EmailDuplicateValidator,
    UsernameDuplicateValidator,
    PhoneNumberValidator,
    UsernameValidator,
    RoleValidator,
    PasswordValidator
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# User Registration Endpoint
@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserLoginResponse
)
async def register(
    request: Request,
    response: Response,
    user: User,
    access_token_se_p3: str = Depends(check_current_user),
):
    if access_token_se_p3:
        user = await get_current_user(access_token_se_p3)
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return {"username": user.username, "role": user.role}

    user.email = user.email.lower()
    handler = EmailValidator()
    handler.escalate_request(EmailDuplicateValidator()).escalate_request(UsernameValidator()).escalate_request(UsernameDuplicateValidator()).escalate_request(PhoneNumberValidator()).escalate_request(RoleValidator()).escalate_request(PasswordValidator())
    dict_user = user.model_dump()
    handler.handle_request(dict_user)

    # Create User and Set Session
    create_user(user.model_dump())

    access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(key="access_token_se_p3", value=access_token, httponly=True)

    return {"username": user.username, "role": user.role}


# User Login Endpoint
@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    access_token_se_p3: str = Depends(check_current_user),
):
    if access_token_se_p3:
        response.delete_cookie("access_token_se_p3")

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
            headers={"set-cookie": ""},
        )

    # Create Access Token and Set Cookie
    new_access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(key="access_token_se_p3", value=new_access_token, httponly=True)

    return {"username": user.username, "role": user.role}


# Get Current User Endpoint
@router.get("/details", response_model=User, status_code=status.HTTP_200_OK)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# Get current user or not
@router.get(
    "/current", response_model=UserLoginResponse, status_code=status.HTTP_200_OK
)
async def check_user(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username, "role": current_user.role}


# User Logout
@router.post("/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(response: Response, current_user: User = Depends(get_current_user)):
    response.delete_cookie("access_token_se_p3")
    return {"message": "Logged Out Successfully"}


# Change Password
@router.post("/change-password", status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    request: Request,
    response: Response,
    passwords: ChangePasswordInput,
    current_user: User = Depends(get_current_user),
):
    user = authenticate_user(current_user.username, passwords.current_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    update_user_password(current_user.username, passwords.new_password)

    # Create Access Token and Set Cookie
    new_access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(key="access_token_se_p3", value=new_access_token, httponly=True)

    return {"message": "Password changed successfully!"}


# User Registration Endpoint
@router.put("/edit", status_code=status.HTTP_202_ACCEPTED)
async def edit(
    request: Request,
    response: Response,
    user: UserEditInput,  # type: ignore
    current_user: User = Depends(get_current_user),
):
    # Check if user email already exists
    user.email = user.email.lower()
    if user.email != current_user.email and get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )
    
    # Check if user username already exists
    if user.username != current_user.username and get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already registered"
        )

    handler = PhoneNumberValidator()
    dict_user = {}
    dict_user['contact'] = user.contact
    handler.handle_request(dict_user)

    # Update the fields from user1 to current_user
    for key, value in user.model_dump().items():
        setattr(current_user, key, value)

    # convert current user to dict
    new_user = current_user.model_dump()

    changed = update_user(new_user)

    if not changed:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user details",
        )

    return {"message": "User details updated successfully!"}
