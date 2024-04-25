import requests
import time
import threading
import json


INSTANCES = 1000


def login(username, password):
    url = "http://localhost/api/users/login"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    return response.cookies


def logout(cookies):
    url = "http://localhost/api/users/logout"
    response = requests.post(url, cookies=cookies)
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
        print("Logged out successfully.")
    else:
        print("Failed to logout.")


def create_listing(cookies, id):
    start_time = time.time()
    url = "http://localhost/api/listings/make_listing"
    listing_name = f"listing_{id:04d}"
    payload = {"name": listing_name}
    payload = json.dumps(payload)
    response = requests.post(url, data=payload, cookies=cookies)
    # if response.status_code == 200 or response.status_code == 201:
    #     print(f"Listing {listing_name} created successfully.")
    # else:
    #     print(response.json())
    #     print(f"Failed to create listing {listing_name}.")
    end_time = time.time()

    if id == 1:
        latency = response.elapsed.total_seconds()
        print(f"Time taken for creating listing {id}: {end_time - start_time}")
        print(f"Latency: {latency}")
        print()


def apply_listing(cookies, username, id):
    start_time = time.time()
    url = "http://localhost/api/applications/apply"
    payload = {
        "user": username,
        "listing": f"listing_{id:04d}",
        "twitter_id": "https://twitter.com/ravikamehta",
        "linkedin_id": "http://linkedin.com/in/bhavberi",
    }
    payload = json.dumps(payload)
    response = requests.post(url, data=payload, cookies=cookies)
    # if response.status_code == 200 or response.status_code == 201 or response.status_code == 202:
    #     print(f"Application for listing {id} submitted successfully.")
    # else:
    #     print(f"Failed to submit application for listing {id}.")
    end_time = time.time()

    if id == 1:
        latency = response.elapsed.total_seconds()
        print(f"Time taken for applying listing {id}: {end_time - start_time}")
        print(f"Latency: {latency}")
        print()


def get_report(cookies, username, id):
    start_time = time.time()
    url = "http://localhost/api/applications/get_report"
    payload = {"username": username, "listing": f"listing_{id:04d}"}
    payload = json.dumps(payload)

    response = requests.post(url, cookies=cookies, data=payload)
    # if response.status_code == 200:
    #     print("Report received successfully.")
    # else:
    #     print("Failed to receive report.", response.status_code)
    end_time = time.time()

    if id == 1:
        latency = response.elapsed.total_seconds()
        print(f"Time taken for getting report {id}: {end_time - start_time}")
        print(f"Latency: {latency}")

# ----------------------------------------------------------------------------


cookies = login("admin", "admin")

listing_threads = []

starttime = time.time()
for i in range(INSTANCES):
    t = threading.Thread(target=create_listing, args=(cookies, i))
    listing_threads.append(t)
    t.start()

for t in listing_threads:
    t.join()

endtime = time.time()
print("Total time taken for creating 1000 listings: ", endtime - starttime)
print("Throughput: ", 1000 / (endtime - starttime))
print()
logout(cookies)

# ----------------------------------------------------------------------------

cookies = login("username", "password")

application_threads = []

starttime = time.time()
for i in range(INSTANCES):
    t = threading.Thread(target=apply_listing, args=(cookies, "username", i))
    application_threads.append(t)
    t.start()

for t in application_threads:
    t.join()

endtime = time.time()
print("Total time taken for applying to 1000 listings: ", endtime - starttime)
print("Throughput: ", 1000 / (endtime - starttime))
print()
logout(cookies)

# ----------------------------------------------------------------------------

cookies = login("recruiter", "recruiter")

report_threads = []

starttime = time.time()
for i in range(50):
    t = threading.Thread(target=get_report, args=(cookies, "username", i))
    report_threads.append(t)
    t.start()

for t in report_threads:
    t.join()

endtime = time.time()
print("Total time taken for getting 50 reports: ", endtime - starttime)
print("Throughput: ", 50 / (endtime - starttime))

logout(cookies)
