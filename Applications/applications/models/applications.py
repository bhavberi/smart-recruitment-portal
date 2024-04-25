from pydantic import BaseModel


class Listing(BaseModel):
    name: str


class Application(BaseModel):
    user: str
    listing: str
    accepted: bool = False
    twitter_id: str
    linkedin_id: str


class Report(BaseModel):
    user: str | None = None
    llama: str | None = None
    mbti: str | None = None
    sentiment: str | None = None
    skills: str | None = None
