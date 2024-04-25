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

st.session_state['report_response'] = response

# st.write(response.status_code)
# st.write(response.content)

if response.status_code == 200:
    report = json.loads(response.content)

    columns1 = st.columns(2)
    columns1[0].markdown("Name")
    columns1[1].markdown(f"{report['user']}")
    

    st.markdown("---")
    st.header("MBTI Results")
    columns2 = st.columns(2)
    columns2[0].write("Personality")
    columns2[1].write(report['mbti']['personality'])

    columns2[0].write("Probability")
    columns2[1].write(report['mbti']['probability'])
    
    
    st.markdown("---")
    st.header("Llama Results")
    st.markdown(report['llama'])
    
    
    st.markdown("---")
    st.header("Sentiment Results")
    columns3 = st.columns(2)
    columns3[0].write("Score")
    
    columns3[1].write(f"Positive: {(report['sentiment']['score']['positive'])}")
    columns3[1].write(f"Neutral: {(report['sentiment']['score']['neutral'])}")
    columns3[1].write(f"Negative: {(report['sentiment']['score']['negative'])}")
    columns3[1].write(f"No Hate: {(report['sentiment']['score']['nohate'])}")
    columns3[1].write(f"Hate: {(report['sentiment']['score']['hate'])}")
    columns3[1].write(f"Non-misogyny: {(report['sentiment']['score']['nonmisogyny'])}")
    columns3[1].write(f"Misogyny: {(report['sentiment']['score']['misogyny'])}")
        
    columns4 = st.columns(2)
    columns4[0].write("Controversial Statements")
    
    if report['sentiment']['controversial'] == []:
        columns4[1].write("No controversial statements found.")
        
    if report['sentiment']['controversial'] != []:
        for statement in report['sentiment']['controversial']:
            if statement is not None: columns4[1].write(statement) 
        
        
    st.markdown("---")
    st.header("Skills")
    skills = json.loads(report['skills'])
    columns5 = st.columns(2)
    columns5[0].write("Occupation")
    columns5[1].write("Probability")
    for skill in skills:
        columns5[0].write(skill)
        columns5[1].write(skills[skill])
    
        
    if st.session_state['application_report']['status'] != "pending":
        st.success(f"This application has already been {st.session_state['application_report']['status']}.")
        st.stop()
        
    st.markdown("---")
        
    columns6 = st.columns(2)
    if columns6[0].button("Accept", key="accept"):
        url = "http://localhost/api/applications/approve"        
        response = requests.put(url, data=payload, headers=headers, cookies=get_all_cookies())
        
        st.write(response.status_code)
        
        if response.status_code == 202:
            st.success("Application accepted.")
        else:
            st.error("An error occurred.")
            
    if columns6[1].button("Reject", key="reject"):
        url = "http://localhost/api/applications/reject"
        response = requests.put(url, data=payload, headers=headers, cookies=get_all_cookies())
        
        st.write(response.status_code)
        
        if response.status_code == 202:
            st.success("Application rejected.")
        else:
            st.error("An error occurred.")

    
else:
    st.error("An error occurred.")