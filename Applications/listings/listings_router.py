from fastapi import APIRouter, Depends, HTTPException, status
from os import getenv

from models.listings import Listing
from models.listings_otypes import (
    ListingResponse,
    Listings,
)
from utils import (
    create_listing,
    remove_listing,
    get_all_listings,
    get_user,
)

from validation import (
    AdminValidator,
    ListingValidator,
    ExistingListingValidator,
)

router = APIRouter()
INTER_COMMUNICATION_SECRET = getenv("INTER_COMMUNICATION_SECRET", "inter-communication-secret")

# make listing
@router.post(
    "/make_listing", status_code=status.HTTP_201_CREATED, response_model=ListingResponse
)
async def make_listing(
    listing: Listing,
    user=Depends(get_user),
):
    handler = AdminValidator()
    handler.escalate_request(ListingValidator())
    request = {"listing": listing.name, "role": user["role"]}
    handler.handle_request(request)

    # create listing
    create_listing(listing.model_dump())

    return {"name": listing.name}


# Get Listing
@router.post(
    "/get_listing", status_code=status.HTTP_200_OK, response_model=ListingResponse
)
async def get_listing(
    listing: Listing,
    secret: str | None = None
):
    if secret != INTER_COMMUNICATION_SECRET:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unauthorized Access",
        )
    
    handler = ExistingListingValidator()
    request = {"listing": listing.name}
    handler.handle_request(request)

    return {"name": listing.name}


# delete listing
@router.delete("/delete_listing", status_code=status.HTTP_200_OK)
async def delete_listing(
    listing: Listing,
    user=Depends(get_user),
):
    handler = AdminValidator()
    handler.escalate_request(ExistingListingValidator())
    request = {"listing": listing.name, "role": user["role"]}
    handler.handle_request(request)

    # delete listing
    remove_listing(listing.name)

    return {"name": listing.name}


# Get all the listings
@router.get("/get_listings", status_code=status.HTTP_200_OK, response_model=Listings)
async def get_listings(
    user=Depends(get_user),
):
    return Listings(listings=get_all_listings())
