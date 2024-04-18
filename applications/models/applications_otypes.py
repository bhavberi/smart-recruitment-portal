from pydantic import BaseModel

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
    applications: list  # validate if this is correct

class ApplicationInput(BaseModel):
    user: str
    listing: str
    twitter_id: str
    linkedin_id: str

class Listings(BaseModel):
    listings: list  # validate if this is correct