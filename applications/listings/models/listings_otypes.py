from pydantic import BaseModel
from typing import List

from models.applications import Listing, Application

class ListingResponse(BaseModel):
    name: str

class Listings(BaseModel):
    listings: List[Listing]