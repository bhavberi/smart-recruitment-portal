import streamlit as st
from streamlit_cookies_controller import CookieController
import requests
import json

st.set_page_config(
    page_title="Login",
    page_icon="👋",
)

def get_all_cookies():
    controller = CookieController()
    
    all_cookies = controller.getAll()
    for cookie in all_cookies:
        if type(all_cookies[cookie]) == type({'a': 1}):
            all_cookies[cookie] = json.dumps(all_cookies[cookie])
    
    return all_cookies

st.title("Login")

if "access_token_se_p3" in get_all_cookies():
    url = "http://localhost/api/users/current"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers, cookies=get_all_cookies())

    username = json.loads(response.content)["username"]
    role = json.loads(response.content)["role"]

    st.session_state["logged_in_user"] = username
    st.session_state["logged_in_role"] = role

    st.write(f"You are already logged in, {role} {username}.")
    st.stop()

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

if "logged_in_role" not in st.session_state:
    st.session_state["logged_in_role"] = None

if st.session_state["logged_in_user"] is not None:
    st.write("You are already logged in.")
    st.stop()

username = st.text_input("Username")
password = st.text_input("Password", type="password")
submit = st.button("Submit")

if submit:
    url = "http://localhost/api/users/login"
    # sending the data as form data
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(url, data=payload, headers=headers)
    
    controller = CookieController()
    for cookie in response.cookies:
        controller.set(cookie.name, str(cookie.value))

    if response.status_code != 200:
        if username != "" and password != "":
            st.write(json.loads(response.text)["detail"])

    else:
        # st.write(f"Successfully logged in, {username}!")
        st.success(f"Successfully logged in, {username}!")
        
        st.session_state["logged_in_user"] = username
        st.session_state["logged_in_role"] = json.loads(response.content)["role"]
        st.session_state['report_data'] = None
        
