from flask import Flask
from os import getenv, system
import json
import regex as re

DEBUG = getenv("DEBUG", "False").lower() in ("true", "1", "t")
SECRET_KEY = getenv("SECRET_KEY", "secret-key")
PORT = int(getenv("PORT", 8080))
OUTPUT_FILENAME = getenv("OUTPUT_FILENAME", "output.txt")
linkedin_regex = "http(s)?://([w]+.)?linkedin.com/(?:company/|in/)[A-z0-9_-]+/?"

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/")
def index():
    return "Backend Service for Linkedin"


@app.route("/ping")
def ping():
    return {"message": "Backend Running!!"}


@app.route("/skills", defaults={"linkedin_link": None})
@app.route("/skills/<path:linkedin_link>")
def skills(linkedin_link):
    if not linkedin_link:
        return {"message": "Please provide a linkedin profile link"}
    if not re.match(linkedin_regex, linkedin_link):
        return {"message": "Invalid Linkedin Profile Link"}

    system(
        f"python3 scraper_linkedin/linkedin.py --profile_link={linkedin_link} > {OUTPUT_FILENAME}"
    )
    fp = open(OUTPUT_FILENAME, "r")
    jobs = fp.read()
    fp.close()
    system(f"rm {OUTPUT_FILENAME}")

    jobs_index = jobs.find("\n{")
    jobs = jobs[jobs_index:]
    cleaned_string = jobs.replace("\n", "").replace("'", '"')
    return json.loads(cleaned_string)


if __name__ == "__main__":
    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)
