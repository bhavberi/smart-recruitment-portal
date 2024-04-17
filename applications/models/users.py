from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    candidate = "candidate"
    recruiter = "recruiter"

class Address(BaseModel):
    house_no: str
    street: str
    city: str
    state: str
    country: str = "India"
    pincode: str

# User Model
class User(BaseModel):
    username: str
    password: str

    full_name: Optional[str] = None
    email: EmailStr
    contact: str
    address: Address
    
    role: Role = Role.recruiter
