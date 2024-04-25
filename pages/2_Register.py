import streamlit as st
from streamlit_cookies_controller import CookieController
import requests
import json

st.set_page_config(
    page_title="Register",
    page_icon="👋",
)

st.title("Register")

def get_all_cookies():
    controller = CookieController()
    
    all_cookies = controller.getAll()
    for cookie in all_cookies:
        if type(all_cookies[cookie]) == type({'a': 1}):
            all_cookies[cookie] = json.dumps(all_cookies[cookie])
    
    return all_cookies

my_cookies = get_all_cookies()
if "access_token_se_p3" in my_cookies:
    url = "http://localhost/api/users/current"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers, cookies=my_cookies)

    username = json.loads(response.content)["username"]
    role = json.loads(response.content)["role"]

    st.session_state["logged_in_user"] = username
    st.session_state["logged_in_role"] = role
    
if st.session_state["logged_in_user"] is not None:
    st.warning("You are already logged in.")
    st.stop()

params = {
    "First Name": "",
    "Last Name": "",
    "Email": "",
    "Contact no": "",
    "House no": "",
    "Street": "",
    "City": "",
    "State": "",
    "Country": "",
    "Pincode": "",
    "Role": "",
    "Username": "",
    "Password": "",
}

for param in params:
    if param == "Address":
        continue

    if param == "Password":
        params[param] = st.text_input(param, type="password")
    elif param == "Role":
        params[param] = st.radio(
            "Role",
            ["recruiter", "candidate"],
            index=None,
        )
    else:
        params[param] = st.text_input(param)


submit = st.button("Submit")

if submit:
    # st.write(f"Registered successfully")

    payload = {
        "username": params["Username"],
        "password": params["Password"],
        "full_name": params["First Name"] + " " + params["Last Name"],
        "email": params["Email"],
        "contact": params["Contact no"],
        "address": {
            "house_no": params["House no"],
            "street": params["Street"],
            "city": params["City"],
            "state": params["State"],
            "country": params["Country"],
            "pincode": params["Pincode"],
        },
        "role": params["Role"],
    }
    # st.write(payload)
    payload = json.dumps(payload)

    # st.write(f"You have entered: ", payload)

    url = "http://localhost/api/users/register"

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=payload, headers=headers)

    # st.write(response.status_code)
    if response.status_code != 201:
            st.warning(json.loads(response.text)["detail"])

    else:
        # st.write(f"Successfully logged in, {username}!")
        st.success(f"Successfully created account, {params['Username']}!")
        
        controller = CookieController()
        for cookie in response.cookies:
            controller.set(cookie.name, str(cookie.value))
        
        st.session_state["logged_in_user"] = params['Username']
        st.session_state["logged_in_role"] = json.loads(response.content)["role"]
        st.session_state['report_data'] = None
        
        