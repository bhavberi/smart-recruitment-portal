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

st.title("View Listings")
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
    
# add verification for type of user

url = "http://localhost/api/listings/get_listings"

headers = {"Content-Type": "application/json"}
response = requests.get(url, headers=headers, cookies=get_all_cookies())

# st.write(response.content)

listings = json.loads(response.text)['listings']
listings = [listing['name'] for listing in listings]

if listings:
    for listing in listings:
        st.write(f"{listing}")
        
else:
    st.write("No listings available.")