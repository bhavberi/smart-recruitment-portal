from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import re
import ast

from models.users import User
from models.users_otypes import UserLoginResponse, ChangePasswordInput, UserEditInput
from utils import (
    check_current_user,
    get_current_user,
    check_phone_number,
    validate_role,
    get_user_by_email,
    get_user_by_username,
    create_user,
    authenticate_user,
    update_user,
    update_user_password,
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
    username: str = Depends(check_current_user),
):
    if username:
        response.status_code = status.HTTP_304_NOT_MODIFIED
        return {"username": username}

    user.email = user.email.lower()

    # Check if user already exists
    if get_user_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already registered"
        )
    if get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    if bool(re.match("^[a-zA-Z0-9]*$", user.username)) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username should only contain alphanumeric characters",
        )

    check_phone_number(user.contact)
    validate_role(user.role)

    # Create User and Set Session
    create_user(user.model_dump())

    request.session["username"] = user.username

    return {"username": user.username}


# User Login Endpoint
@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserLoginResponse)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    username: str = Depends(check_current_user),
):
    if username:
        request.session.pop("username", None)

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
            headers={"set-cookie": ""},
        )

    # Set Session
    request.session["username"] = user.username

    return {"username": user.username}


# Get Current User Endpoint
@router.get("/details", response_model=User, status_code=status.HTTP_200_OK)
async def read_users_me(
    request: Request, current_user: User = Depends(get_current_user)
):
    return current_user


# Get current user or not
@router.get(
    "/current", response_model=UserLoginResponse, status_code=status.HTTP_200_OK
)
async def check_user(request: Request, username: str = Depends(check_current_user)):
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return {"username": username}


# User Logout
@router.post("/logout", status_code=status.HTTP_202_ACCEPTED)
async def logout(request: Request, current_user: User = Depends(get_current_user)):
    request.session.pop("username", None)
    return {"message": "Logged Out Successfully"}


# Change Password
@router.post("/change-password", status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    request: Request,
    passwords: ChangePasswordInput,
    current_user: User = Depends(get_current_user),
):
    user = authenticate_user(current_user.username, passwords.current_password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
        )

    update_user_password(current_user.username, passwords.new_password)

    # Set Session
    request.session["username"] = user.username

    return {"message": "Password changed successfully!"}


# User Registration Endpoint
@router.put("/edit", status_code=status.HTTP_202_ACCEPTED)
async def edit(
    request: Request,
    response: Response,
    user: UserEditInput,
    current_user: User = Depends(get_current_user),
):
    # Check if user email already exists
    user.email = user.email.lower()
    if user.email != current_user.email and get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    check_phone_number(user.contact)

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
