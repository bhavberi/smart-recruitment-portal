# LinkedIn Data Scraping Service

To run this service, you need to firstly make a virtual environment and install the requirements. You can do this by running the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Now, you need to set the environment variables. You can do this by copying the `.env.example` file to `.env` and filling in the required values.

```bash
cp .env.example .env
```

Then, set the LINKEDIN Crednetials in the env file.

After installing the requirements and setting the environment variables, you can run the service by running the following command:

```bash
python3 app.py
```

- Now, you can check the service by sending a request to `http://localhost:8080/linkedin/<linkedin_url>`.

    An example of it would be `http://localhost:8080/skills/http://linkedin.com/in/bhavberi`.