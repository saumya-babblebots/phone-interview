import streamlit as st
import requests
import time
import prompts
import config
from region_voices import REGION_VOICES

st.markdown("# Initiate a call ")  
st.sidebar.markdown("# Babblebots ")

auth_token = st.secrets["auth_token"]
phone_number_id = st.secrets["phone_number_id"]


# Create the header with Authorization token
headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json',
}

def create_payload(company, questions, candidate_phone_number, candidate_name, role, region, selected_template):
    # Create the payload for the API request
    # if not candidate_name:
    #     candidate_name = "there"
        
    config.stt_model["keywords"] = [company, candidate_name]
    config.llm["messages"][0]["content"] = prompts.system_prompt.format(company=company)
    config.llm["messages"][1]["content"] = prompts.user_prompt.format(questions=questions, company=company)
    if (selected_template in ("Car Salesman", "Software Engineer")) or (role.lower() in ("car salesman", "software engineer")):
        config.llm['messages'][1]['content'] = prompts.user_prompt_with_probing.format(questions=questions, company=company)
        
    if region == 'India':
        recruiter = "Tina"
    else:
        recruiter = "Eric"
        
    voice_settings = REGION_VOICES.get(region,REGION_VOICES['US'])
    
    data = {
        'assistant': {
            "firstMessage": prompts.first_bot_message.format(company=company, candidate_name=candidate_name, role=role, recruiter=recruiter),
            #"endCallMessage": prompts.end_call_message.format(candidate_name=candidate_name),
            "endCallPhrases": ["Have a great day."],
            "backgroundDenoisingEnabled": True,
            "responseDelaySeconds": 0.8,
            "silenceTimeoutSeconds": 30,
            "transcriber": config.stt_model,
            "model": config.llm,
            "startSpeakingPlan": {
                "waitSeconds": 0.8
            },
            "endCallFunctionEnabled": True,
            "voice":  voice_settings,
            "backgroundSound": "off"
        },
        'phoneNumberId': phone_number_id,
        'customer': {
            'number': candidate_phone_number,
        },
    }

    return data

region = st.selectbox(
    label="Select the region",
    options=list(REGION_VOICES.keys())  
)

if 'call_id' not in st.session_state:
    st.session_state.call_id = None
    
if 'recording_button_clicked' not in st.session_state:
    st.session_state.recording_button_clicked = True

def show_questions():
    selected_option = st.session_state.questions_dropdown
    print(f"Selected option: {selected_option}")
    if selected_option:
        st.session_state.questions_text = prompts.interview_questions["_".join(selected_option.lower().split())]
    else:
        st.session_state.questions_text = ""

def create_call(data):
    # Make the POST request to VAPI to create the phone call
    try: 
        response = requests.post(
            'https://api.vapi.ai/call', headers=headers, json=data
        )

        # Check if the request was successful
        if response.text:
            if response.status_code == 201:
                print('Call created successfully')
                st.session_state.call_id = response.json().get('id', None)
                print(response.json())
            else:
                print('Failed to create call')
                print(response.text)
        else:
            print("No data received to create call")
    except Exception as e:
        print('Error creating call')
        print("Error: ", e)


def get_call_id():
    return st.session_state.get('call_id', None)

company = st.text_input(
    label="Enter the name of the company that the AI assistant is calling on behalf of",
    #value="AMS"
)

candidate_name = st.text_input(
    label="Enter the first name of the candidate here ",
    # value="AMS"
)

role = st.text_input(
    label="Enter the role that the candidate is being interviewed for",
)

selected_template = st.selectbox(
    "Choose the interview questions from one of these templates or type out your own below",
    (
        "Retail Appointment Generator", 
        "Warehouse Operator", 
        "Onboarding flow asking for signed contract", 
        "Onboarding flow asking for work history",
        "Channel Sales Manager",
        "Software Engineer",
        "Nurse Practitioner",
        "Car Salesman"
    ),
    index=None,
    on_change=show_questions,
    key="questions_dropdown"
)

questions = st.text_area(
    label="Enter the questions here",
    height=200,
    key="questions_text"
)


phone_number = st.text_input(
    label="Enter the candidate's phone number here in the given format ('+' followed by the country-code and mobile-number with no spaces in-between )",
    placeholder="+18888888888",
)


if st.button("Make the call", type="primary"):
    try:
        data = create_payload(company, questions, phone_number, candidate_name, role, region, selected_template)
        if(data):
            create_call(data)
            with st.empty():
                st.write("The AI assistant is calling the above number now.")
                time.sleep(5)
                st.write("")
            st.session_state.recording_button_clicked = False
        else:
            print("No payload recieved for creating call")
    except Exception as e:
        print("Error creating call: ", e)

    
st.markdown("# ")
if st.button("Interview Recording", type="primary", disabled=st.session_state.recording_button_clicked):
    call_id = get_call_id()
    if call_id:    
        url = f"https://api.vapi.ai/call/{call_id}"
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            recording = response.json().get("recordingUrl",None)
            print(recording)
        
            if recording:
                st.markdown("# ")
                st.audio(recording)
            else: 
                st.warning("No recording found or call is still in progress!")
        else:
            st.error(f"failed to fetch interview details {response.status_code} - {response.text}")
        
    else:
        st.info("Call id not found, please make a call first")
