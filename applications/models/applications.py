from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class Listing(BaseModel):
    name: str

class Application(BaseModel):
    user: str
    listing: str
    accepted: bool  # how to set default to false?
    twitter_id: str
    linkedin_id: str

class Report(BaseModel):
    user: str
    llama: str
    mbti: str
    sentiment: str
    report_gen: str