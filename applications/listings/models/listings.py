from pydantic import BaseModel
from typing import Optional

class Listing(BaseModel):
    name: str