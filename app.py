import streamlit as st
import requests
import time
import prompts
import config

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
    data = {
        'assistant': config.get_assistant(selected_template, region, company, candidate_name, role, questions),
        'phoneNumberId': phone_number_id,
        'customer': {
            'number': candidate_phone_number,
        },
    }

    return data

region = st.selectbox(
    label="Select the region",
    options=list(config.REGION_VOICES.keys())  
)

if 'call_id' not in st.session_state:
    st.session_state.call_id = None
    
if 'recording_button_clicked' not in st.session_state:
    st.session_state.recording_button_clicked = True

if 'transcript_button_clicked' not in st.session_state:
    st.session_state.transcript_button_clicked = True

def show_questions():
    selected_option = st.session_state.questions_dropdown
    print(f"Selected option: {selected_option}")
    if selected_option:
        st.session_state.questions_text = prompts.interview_questions["_".join(selected_option.lower().split())]
        if "Onboarding flow" not in selected_option:
            st.session_state.role_name = selected_option
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
    value="AmeriForce"
)

candidate_name = st.text_input(
    label="Enter the first name of the candidate here",
)

selected_template = st.selectbox(
    "Choose the interview questions from one of these templates or type out your own below",
    (
        "Structural Coatings - Material Handler",
        "Hurricane Clean-Up Labor",
        "Retail Appointment Generator", 
        "Warehouse Operator", 
        "Onboarding flow asking for signed contract", 
        "Onboarding flow asking for work history",
        "Channel Sales Manager",
        "Software Engineer",
        "Nurse Practitioner",
        "Car Salesman"
    ),
    index=0,  # None,
    on_change=show_questions,
    key="questions_dropdown"
)

questions = st.text_area(
    label="Enter the questions here",
    height=200,
    key="questions_text",
    value=prompts.material_handler
)

role = st.text_input(
    label="Enter the role that the candidate is being interviewed for",
    key="role_name",
    value="Structural Coatings - Material Handler"
)

phone_number = st.text_input(
    label="Enter the candidate's phone number here in the given format ('+' followed by the country-code and mobile-number with no spaces in-between )",
    placeholder="+18888888888"
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
            st.session_state.transcript_button_clicked = False
        else:
            print("No payload recieved for creating call")
    except Exception as e:
        print("Error creating call: ", e)

    
