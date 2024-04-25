from os import getenv
from pymongo import MongoClient
from passlib.context import CryptContext

SECRET_KEY = getenv("JWT_SECRET_KEY", "this_is_my_very_secretive_secret") + "__d7__"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# get mongodb URI and database name from environment variale
MONGO_URI = "mongodb://{}:{}@{}:{}/".format(
    getenv("MONGO_USERNAME", default="username"),
    getenv("MONGO_PASSWORD", default="password"),
    getenv("MONGO_CONNECTION_NAME", default="localhost"),
    getenv("MONGO_PORT", default="27017"),
)
MONGO_DATABASE = getenv("MONGO_DATABASE", default="mydb")

# instantiate mongo client
client = MongoClient(MONGO_URI, uuidRepresentation="standard")

# get database
db = client[MONGO_DATABASE]

try:
    # check if the clubs index exists
    if "unique_username" in db.users.index_information():
        print("The username index exists in users.")
    else:
        # create the index
        db.users.create_index([("username", 1)], unique=True, name="unique_username")
        print("The username index was created in users.")

    print(db.users.index_information())

    if db.users.find_one({"role": "admin"}):
        print("User with admin role exists.")
    else:
        ADMIN_PASSWORD = getenv("ADMIN_PASSWORD", default="admin")
        db.users.insert_one({
            "username": "admin", 
            "password": pwd_context.hash(ADMIN_PASSWORD),
            "role": "admin",
            "email": "admin@admin.in",
            "contact": "9999999999",
            "address": {
                "house_no": "123",
                "street": "admin street",
                "city": "admin city",
                "state": "admin state",
                "country": "admin country",
                "pincode": "123456"
            }
        })
        print("The admin user was created.")
except Exception:
    pass
