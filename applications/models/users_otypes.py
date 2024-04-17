from pydantic import BaseModel, create_model
from .users import User

# User Login Model
class UserLogin(BaseModel):
    username: str
    password: str


# User Login Response Model
class UserLoginResponse(BaseModel):
    username: str


# Change Password Input Model
class ChangePasswordInput(BaseModel):
    current_password: str
    new_password: str

# def create_user_input_fields(exclude_fields = []):
#     all_fields = User.__annotations__.items()

#     new_fields = {}

#     for name, type_ in all_fields:
#         if name not in exclude_fields:
#             new_fields[name] = (type_, ...)

#     return create_model(
#         "UserEditInput",
#         **new_fields
#     )

# UserEditInput = create_user_input_fields(['username', 'role', 'password'])

UserEditInput = create_model(
    "UserEditInput",
    **{name: (type_, ...) for name, type_ in User.__annotations__.items() if name not in {'username', 'role', 'password'}} # type: ignore
) # type: ignore

