import streamlit as st
from streamlit_cookies_controller import CookieController
import requests
import json

def get_all_cookies():
    controller = CookieController()
    
    all_cookies = controller.getAll()
    for cookie in all_cookies:
        if isinstance(all_cookies[cookie], dict):
            all_cookies[cookie] = json.dumps(all_cookies[cookie])
    
    return all_cookies

st.title("View Applications")

# Check if user is logged in
my_cookies = get_all_cookies()
if "access_token_se_p3" not in my_cookies:
    st.warning("You need to login first.")
    st.stop()

# Verify user role
url = "http://localhost/api/users/current"
headers = {"Content-Type": "application/json"}
response = requests.get(url, headers=headers, cookies=my_cookies)

if response.status_code != 200:
    st.warning("Failed to retrieve user data.")
    st.stop()

user_data = json.loads(response.content)
logged_in_role = user_data.get("role")

if logged_in_role not in ["recruiter", "admin"]:
    st.warning("You need to be a recruiter to view applications.")
    st.stop()

# Input for listing name
listing_name = st.text_input("Listing Name")
submit = st.button("Search")

if submit:
    url = "http://localhost/api/applications/get_applications"
    payload = {"name": listing_name}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, data=json.dumps(payload), headers=headers, cookies=my_cookies)

    if response.status_code != 200:
        st.warning("Failed to retrieve applications.")
        st.stop()

    applications = json.loads(response.text).get('applications', [])

    if not applications:
        st.warning("No applications found.")
        st.stop()

    # Display application details and set session state on button click
    for application in applications:
        st.write(f"User: {application['user']}")
        st.write(f"Listing: {application['listing']}")
        st.write(f"Twitter ID: {application.get('twitter_id', 'N/A')}")
        st.write(f"LinkedIn ID: {application.get('linkedin_id', 'N/A')}")
        button_clicked = st.button(f"Select Application {application['user']}")
        if button_clicked:
            # Set session state with selected application details
            st.session_state['selected_application'] = application
