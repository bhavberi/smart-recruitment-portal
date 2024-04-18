from fastapi import FastAPI
from os import getenv
import users_router

DEBUG = getenv("BACKEND_DEBUG", "False").lower() in ("true", "1", "t")

# Create a new FastAPI instance
# FastAPI App
if DEBUG:
    app = FastAPI(
        debug=DEBUG,
        title="User Management",
        description="User Management Backend for SE Project 3 for the Team 12",
        root_path="/api/users"
    )
else:
    app = FastAPI(
        debug=DEBUG,
        title="User Management",
        description="User Management Backend for SE Project 3 for the Team 12",
        docs_url=None,
        redoc_url=None,
        root_path="/api/users"
    )

# Backend Index Page - For checking purposes
@app.get("/ping", tags=["General"])
async def index():
    return {"message": "Backend Running!!"}

# Mount the user router on the "/user" path
app.include_router(users_router.router, tags=["User"])
