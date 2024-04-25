from pydantic import BaseModel
from typing import List

from models.listings import Listing


class ListingResponse(BaseModel):
    name: str


class Listings(BaseModel):
    listings: List[Listing]
