import streamlit as st
from streamlit_cookies_controller import CookieController
import requests
import json
from streamlit_extras.switch_page_button import switch_page

def get_all_cookies():
    controller = CookieController()
    
    all_cookies = controller.getAll()
    for cookie in all_cookies:
        if type(all_cookies[cookie]) == type({'a': 1}):
            all_cookies[cookie] = json.dumps(all_cookies[cookie])
    
    return all_cookies

st.title("View Applications")
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
if st.session_state["logged_in_role"] not in ["recruiter", "admin"]:
    st.warning("You need to be a recruiter to view applications.")
    st.stop()
    
    
listing_name = st.text_input("Listing Name")
submit = st.button("Search", key="search")

if 'applications' not in st.session_state:
    st.session_state['applications'] = None

if submit:
    url = "http://localhost/api/applications/get_applications"

    payload = {"name": listing_name}
    payload = json.dumps(payload)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=payload, headers=headers, cookies=get_all_cookies())

    if response.status_code == 400:
        st.write("No such listing.")
        st.stop()

    st.session_state['applications'] = json.loads(response.text)['applications']
    
if st.session_state['applications']:
    st.write(f"Applications found for {listing_name}:")
    
    columns = st.columns(2)

    for row_id, application in enumerate(st.session_state['applications']):
        columns[0].markdown(f"{row_id+1}:")
        columns[1].markdown(f"{row_id+1}")
        
        for field in application:
            columns[0].markdown(f"{field}")
            columns[1].markdown(f"{application[field]}")
        
else:
    st.write("No applications found for this listing.")
        

application_number = st.text_input("Enter which application you want the report for")

if st.button("Generate"):
    st.session_state["application_report"] = st.session_state['applications'][int(application_number)-1]
    # st.write(st.session_state['applications'][0])
    st.switch_page("pages/8_Report.py")