from pydantic import BaseModel
from enum import Enum

class Status(str, Enum):
    accepted = "accepted"
    rejected = "rejected"
    pending = "pending"


class Listing(BaseModel):
    name: str


class Application(BaseModel):
    user: str
    listing: str
    status: Status = Status.pending
    twitter_id: str
    linkedin_id: str


class Report(BaseModel):
    user: str | None = None
    llama: str | None = None
    mbti: str | None = None
    sentiment: str | None = None
    skills: str | None = None
