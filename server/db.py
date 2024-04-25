# from os import getenv
# from dotenv import load_dotenv
# load_dotenv()
# from pymongo import MongoClient

# # get mongodb URI and database name from environment variale
# MONGO_URI = "mongodb+srv://bhavberi:bhavberi@newcluster.wobr631.mongodb.net/"
# MONGO_DATABASE = getenv("MONGO_DATABASE", default="dev")

# # instantiate mongo client
# client = MongoClient(MONGO_URI)

# # get database
# db = client[MONGO_DATABASE]

from os import getenv
from pymongo import MongoClient

# get mongodb URI and database name from environment variale
MONGO_URI = "mongodb://{}:{}@{}:{}/".format(
    getenv("MONGO_USERNAME", default="username"),
    getenv("MONGO_PASSWORD", default="password"),
    getenv("MONGO_CONNECTION_NAME", default="localhost"),
    getenv("MONGO_PORT", default="25235"),
)
MONGO_DATABASE = getenv("MONGO_DATABASE", default="mydb")

# instantiate mongo client
client = MongoClient(MONGO_URI, uuidRepresentation="standard")

# get database
db = client[MONGO_DATABASE]