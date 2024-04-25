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

st.title("Report")
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
if st.session_state["logged_in_role"] not in ["recruiter"]:
    st.warning("You need to be a recruiter to view a report.")
    st.stop()

if 'application_report' not in st.session_state:
    st.warning("Select a report first.")
    st.stop()
    
if 'application_report' not in st.session_state:
    st.error("An error occurred.")
    
# st.write(f"{st.session_state['application_report']}")

url = "http://localhost/api/applications/get_report"

payload = {
  "username": st.session_state['application_report']['user'],
  "listing": st.session_state['application_report']['listing']
}

payload = json.dumps(payload)
headers = {"Content-Type": "application/json"}
response = requests.post(url, data=payload, headers=headers, cookies=get_all_cookies())

# st.write(response)

if response.status_code == 200:
    report = json.loads(response.content)
    
    columns = st.columns(2)
    for field in report:
        columns[0].markdown(f"{field}")
        columns[1].markdown(f"{report[field]}")
        
    if st.session_state['application_report']['status'] != "pending":
        st.success(f"This application has already been {st.session_state['application_report']['status']}.")
        st.stop()
        
    if st.button("Accept", key="accept"):
        url = "http://localhost/api/applications/approve"        
        response = requests.put(url, data=payload, headers=headers, cookies=get_all_cookies())
        
        st.write(response.status_code)
        
        if response.status_code == 202:
            st.success("Application accepted.")
        else:
            st.error("An error occurred.")
            
    if st.button("Reject", key="reject"):
        url = "http://localhost/api/applications/reject"
        response = requests.put(url, data=payload, headers=headers, cookies=get_all_cookies())
        
        st.write(response.status_code)
        
        if response.status_code == 202:
            st.success("Application rejected.")
        else:
            st.error("An error occurred.")

    
else:
    st.error("An error occurred.")