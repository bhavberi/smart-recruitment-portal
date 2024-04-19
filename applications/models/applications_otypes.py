from pydantic import BaseModel

from models.applications import Listing, Application

class ListingResponse(BaseModel):
    name: str

class ApplicationResponse(BaseModel):
    user: str

class UserApplication(BaseModel):
    username: str
    listing: str

class Approval(BaseModel):
    status: bool

class Applications(BaseModel):
    applications: list[Application]

class ApplicationInput(BaseModel):
    user: str
    listing: str
    twitter_id: str
    linkedin_id: str

class Listings(BaseModel):
    listings: list[Listing]