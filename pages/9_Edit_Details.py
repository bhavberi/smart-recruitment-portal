import streamlit as st
from streamlit_cookies_controller import CookieController
import requests
import json

st.set_page_config(
    page_title="Edit Details",
    page_icon="👋",
)

st.title("Edit Details")


def get_all_cookies():
    controller = CookieController()

    all_cookies = controller.getAll()
    for cookie in all_cookies:
        if type(all_cookies[cookie]) == type({"a": 1}):
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

if st.session_state["logged_in_user"] is None:
    st.warning("You are not logged in.")
    st.stop()
    
if st.session_state["logged_in_role"] in ["admin"]:
    st.warning("You are an admin.")
    st.stop()   


url = "http://localhost/api/users/details"
response = requests.get(url, headers=headers, cookies=my_cookies)

params = json.loads(response.content)
# st.write(params)
address_param = params["address"]
for param in address_param:
    params[param] = address_param[param]

fname = params["full_name"].split(" ")[0]
lname = ''

if ' ' in params["full_name"]:
    lname = params["full_name"].split(" ")[1]

params = {
    "First Name": params["full_name"].split(" ")[0],
    "Last Name": lname,
    "Contact no": params["contact"],
    "House no": params["house_no"],
    "Street": params["street"],
    "City": params["city"],
    "State": params["state"],
    "Country": params["country"],
    "Pincode": params["pincode"],
}

# st.write(f"Your current details are: ", params)

for param in params:
    params[param] = st.text_input(param, value=params[param])

submit = st.button("Submit")

if submit:
    
    payload = {
        "full_name": params["First Name"] + " " + params["Last Name"],
        "contact": params["Contact no"],
        "address": {
            "house_no": params["House no"],
            "street": params["Street"],
            "city": params["City"],
            "state": params["State"],
            "country": params["Country"],
            "pincode": params["Pincode"],
        },
    }
    payload = json.dumps(payload)

    # st.write(f"You have entered: ", payload)

    url = "http://localhost/api/users/edit"

    headers = {"Content-Type": "application/json"}
    response = requests.put(url, data=payload, headers=headers, cookies=get_all_cookies())

    # st.write(response.status_code)
    if response.status_code not in [200, 201, 202]:
        st.warning(json.loads(response.content)['detail'])

    else:
        st.success(f"Successfully updated details.")