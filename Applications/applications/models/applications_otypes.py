from pydantic import BaseModel
from typing import List

from models.applications import Application


class ApplicationResponse(BaseModel):
    user: str


class UserApplication(BaseModel):
    username: str
    listing: str


class Approval(BaseModel):
    status: bool


class Applications(BaseModel):
    applications: List[Application]


class ApplicationInput(BaseModel):
    user: str
    listing: str
    twitter_id: str
    linkedin_id: str
