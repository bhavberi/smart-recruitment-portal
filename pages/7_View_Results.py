import streamlit as st
from streamlit_cookies_controller import CookieController
import requests
import json


def get_all_cookies():
    controller = CookieController()

    all_cookies = controller.getAll()
    for cookie in all_cookies:
        if type(all_cookies[cookie]) == type({"a": 1}):
            all_cookies[cookie] = json.dumps(all_cookies[cookie])

    return all_cookies


st.title("View Results")
my_cookies = get_all_cookies()
if "access_token_se_p3" in my_cookies:
    url = "http://localhost/api/users/current"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers, cookies=my_cookies)

    username = json.loads(response.content)["username"]
    role = json.loads(response.content)["role"]

    st.session_state["logged_in_user"] = username
    st.session_state["logged_in_role"] = role

if st.session_state["logged_in_user"] is None:
    st.write("You need to login first.")
    st.stop()

# add verification for type of user
if st.session_state["logged_in_role"] not in ["candidate"]:
    st.warning("You need to be a candidate to view your results.")
    st.stop()

listing_name = st.text_input("Listing Name")
submit = st.button("Search")

if submit:
    url = "http://localhost/api/applications/get_application_status"

    payload = {"username": st.session_state["logged_in_user"], "listing": listing_name}
    payload = json.dumps(payload)
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        url, data=payload, headers=headers, cookies=get_all_cookies()
    )

    if response.status_code == 400:
        st.write("No application found")
        st.stop()

    status = json.loads(response.text)["status"]

    if status is not None:
        if status:
            st.success("Congratulations! Your application was accepted.")

    else:
        st.write("Application not reviewed yet.")
