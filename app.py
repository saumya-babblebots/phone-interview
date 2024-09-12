import streamlit as st
import requests
import prompts

st.markdown("# Initiate a call ")  
st.sidebar.markdown("# Creating a call")

# Your Vapi API Authorization token
auth_token = st.secrets["auth_token"]

# Phone Number ID of the number to be used for calling
phone_number_id = st.secrets["phone_number_id"]


# Create the header with Authorization token
headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json',
}

def create_payload(company, questions, candidate_phone_number, candidate_name, role):
    # Create the payload for the API request
    if not candidate_name:
        candidate_name = "there"
    data = {
        'assistant': {
            "firstMessage": prompts.first_bot_message.format(company=company, candidate_name=candidate_name, role=role),
            "endCallMessage": prompts.end_call_message.format(candidate_name=candidate_name),
            "backgroundDenoisingEnabled": True,
            "responseDelaySeconds": 1.0,
            "silenceTimeoutSeconds": 30,
            "transcriber": {
                "model": "nova-2",
                "language": "en",
                "provider": "deepgram",
                "keywords": [company, candidate_name]
            },
            "model": {
                "provider": "openai",
                "model": "gpt-4o-mini",
                "maxTokens": 150,
                "numFastTurns": 2,
                "messages": [
                    {
                        "role": "system",
                        "content": prompts.system_prompt.format(company=company),
                        "role": "assistant",
                        "content": prompts.user_prompt.format(questions=questions, company=company)
                    }
                ]
            },
            "endCallFunctionEnabled": True,
            "voice":  {
                "model": "eleven_turbo_v2_5",
                "voiceId": "cjVigY5qzO86Huf0OWal", #"orpheus",
                "provider": "11labs", # 'deepgram'
                "stability": 0.5,
                "similarityBoost": 0.75
            },
            "backgroundSound": "off"
        },
        'phoneNumberId': phone_number_id,
        'customer': {
            'number': candidate_phone_number,
        },
    }

    return data

if 'call_id' not in st.session_state:
    st.session_state.call_id = None

def create_call(data):
    # Make the POST request to VAPI to create the phone call
    response = requests.post(
        'https://api.vapi.ai/call/phone', headers=headers, json=data
    )

    # Check if the request was successful
    if response.status_code == 201:
        print('Call created successfully')
        st.session_state.call_id = response.json().get('id', None)
        print(response.json())
    else:
        print('Failed to create call')
        print(response.text)

company = st.text_input(
    label="Enter the name of the company that the AI assistant is calling on behalf of",
    #value="AMS"
)

candidate_name = st.text_input(
    label="Enter the first name of the candidate here (optional)",
    # value="AMS"
)

role = st.text_input(
    label="Enter the role that the candidate is being interviewed for",
)

questions = st.text_area(
    label="Enter the questions here",
    height=300,
    key="questions_text"
)
def get_call_id():
    return st.session_state.get('call_id', None)

def retail_appointment_flow_clicked():
    st.session_state.questions_text = prompts.retail_appointment_generator
    
def warehouse_operator_flow_clicked():
    st.session_state.questions_text = prompts.warehouse_operator_questions

def work_history_flow_clicked():
    st.session_state.questions_text = prompts.work_history_questions

def signed_contract_flow_clicked():
    st.session_state.questions_text = prompts.signed_contract_questions.format(company=company)

def sales_manager_flow_clicked():
    st.session_state.questions_text = prompts.sales_manager_questions

def software_engineer_flow_clicked():
    st.session_state.questions_text = prompts.software_engineer_questions

def nurse_practitioner_flow_clicked():
    st.session_state.questions_text = prompts.nurse_practitioner_questions

st.write("You can also choose from a questions template below")
st.button("Retail Appointment Generator questions", on_click=work_history_flow_clicked)
st.button("Warehouse Operator", on_click=warehouse_operator_flow_clicked)
st.button("Onboarding flow asking for signed contract", on_click=signed_contract_flow_clicked)
st.button("Onboarding flow with work history questions", on_click=work_history_flow_clicked)
st.button("Channel Sales Manager", on_click=sales_manager_flow_clicked)
st.button("Software Engineer", on_click=software_engineer_flow_clicked)
st.button("Nurse Practitioner", on_click=nurse_practitioner_flow_clicked)

phone_number = st.text_input(
    label="Enter the candidate's phone number here in the given format ('+' followed by the country-code and mobile-number with no spaces in-between )",
    placeholder="+18888888888",
)

# st.button("Make the call", type="primary")

# st.write(questions)

if st.button("Make the call", type="primary"):
    data = create_payload(company, questions, phone_number, candidate_name, role)
    st.write("The AI assistant is calling the above number now.")
    create_call(data)

    # print(prompts.user_prompt.format(questions=questions))
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Interview Recording", type="primary"):
    call_id = get_call_id()
    if call_id:    
        url = f"https://api.vapi.ai/call/{call_id}"
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            recording = response.json().get("recordingUrl",None)
            print(recording)
        
            if recording:
                st.markdown("<br>", unsafe_allow_html=True)
                st.audio(recording)
            else: 
                st.warning("No recording found or call is still in progress!")
        else:
            st.error(f"failed to fetch interview details {response.status_code} - {response.text}")
        
    else:
        st.info("Call id not found, please make a call first")
