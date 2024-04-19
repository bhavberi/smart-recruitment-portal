from pydantic import BaseModel
from typing import Optional

class Listing(BaseModel):
    name: str

class Application(BaseModel):
    user: str
    listing: str
    accepted: bool
    twitter_id: str
    linkedin_id: str

class Report(BaseModel):
    user: str
    llama: str
    mbti: str
    sentiment: str
    report_gen: str