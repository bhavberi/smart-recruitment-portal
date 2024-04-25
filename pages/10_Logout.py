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

st.set_page_config(
    page_title="Log Out",
    page_icon="👋",
)

st.title("Log out")

my_cookies = get_all_cookies()
if "access_token_se_p3" in my_cookies:
    url = "http://localhost/api/users/current"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers, cookies=my_cookies)

    username = json.loads(response.content)["username"]
    role = json.loads(response.content)["role"]

    st.session_state["logged_in_user"] = username
    st.session_state["logged_in_role"] = role
else:
    st.write("Not logged in.")
    st.stop()

if st.session_state["logged_in_user"] is None:
    st.write("Not logged in.")
    st.stop()


st.write(f"You are currently logged in as {st.session_state['logged_in_role']} {st.session_state['logged_in_user']}")
st.write("Do you want to log out?")

submit = st.button("Log out")

if submit:
    url = "http://localhost/api/users/logout"
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, cookies=get_all_cookies())
    
    if response.status_code != 202:
        st.write(json.loads(response.text))
        
    else:
        st.success(f"Successfully logged out!") 
        
        st.session_state["logged_in_user"] = None
        st.session_state["logged_in_role"] = None
        
        st.cache_data.clear()
        st.cache_resource.clear()
        
        controller = CookieController()
        all_cookies = controller.getAll()
        
        for cookie in list(all_cookies):
            controller.remove(cookie)
    