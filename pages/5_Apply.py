import streamlit as st
from streamlit_cookies_controller import CookieController
import requests
import json

def get_all_cookies():
    controller = CookieController()
    
    all_cookies = controller.getAll()
    for cookie in all_cookies:
        if type(all_cookies[cookie]) == type({'a': 1}):
            all_cookies[cookie] = json.dumps(all_cookies[cookie])
    
    return all_cookies

st.title("Apply")
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
    st.warning("You need to login first.")
    st.stop()

if st.session_state["logged_in_role"] not in ["candidate"]:
    st.warning("You need to be a candidate to apply.")
    st.stop()
    
params = {"Listing Name": "", "Twitter ID": "", "LinkedIn ID": ""}

for param in params:
    params[param] = st.text_input(param)

submit = st.button("Submit")

if submit:
    params["user"] = st.session_state["logged_in_user"]

    url = "http://localhost/api/applications/apply"

    payload = {
        "user": st.session_state["logged_in_user"],
        "listing": params["Listing Name"],
        "twitter_id": params["Twitter ID"],
        "linkedin_id": params["LinkedIn ID"],
    }
    payload = json.dumps(payload)

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        url, data=payload, headers=headers, cookies=get_all_cookies()
    )

    if response.status_code not in [200, 201]:
        st.write(json.loads(response.text)["detail"])

    else:
        st.write(f"Successfully applied to listing: {params['Listing Name']}")
