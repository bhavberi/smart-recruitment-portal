from pydantic import BaseModel


class Listing(BaseModel):
    name: str
