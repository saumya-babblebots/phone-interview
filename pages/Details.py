import requests
import streamlit as st
from app import get_call_id

st.markdown("# Get call details ")  
st.sidebar.markdown("# Babblebots ")

auth_token = st.secrets["auth_token"]
phone_number_id = st.secrets["phone_number_id"]

call_id = get_call_id()

headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json',
}

if 'recording_button_clicked' not in st.session_state:
    st.session_state.recording_button_clicked = True
    
if 'transcript_button_clicked' not in st.session_state:
    st.session_state.transcript_button_clicked = True

    
def get_call_audio(call_id):
    url = f"https://api.vapi.ai/call/{call_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code==200:
        try:
            recording = response.json().get("recordingUrl",None)
            print(recording)
            return(recording)
        except Exception as e:
            print("Error could not find recording of inteview", e)
    else:
        return f"Failed to fetch transcript: {response.status_code} - {response.text}"
    

def get_call_transcript(call_id):
    url = f"https://api.vapi.ai/call/{call_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            response_data = response.json()
            #print(response_data)
            data = response_data.get("messages", [])
            #print(data)
            if data:
                intro = data[1]['message'].split('\n')[-1]
                transcript = f"Role: bot, Message: {intro}\n"

                for item in data[2:]:
                    role = item['role']
                    message = item['message']
                    transcript += f"Role: {role}, Message: {message}\n"
                    #print(transcript)
                
                return transcript
            else:
                return "No transcript data available."
        except Exception as e:
            return f"Error while parsing transcript: {e}"
    else:
        return f"Failed to fetch transcript: {response.status_code} - {response.text}"
    

st.markdown("# ")    
if st.button("Get Transcript",type="primary", disabled=st.session_state.transcript_button_clicked):
    try:
        if call_id:
            transcript = get_call_transcript(call_id)
            st.session_state.transcript = transcript  # Save transcript in session state
            #st.session_state.transcript_button_clicked = True
        else:
            st.warning("No call ID found. Please make a call first.")
    except Exception as e:
        print("Error fetching transcript: ", e)


if st.button("Interview Recording", type="primary", disabled=st.session_state.recording_button_clicked):
    try:
        if call_id:
            recording = get_call_audio(call_id)
            st.session_state.recording = recording  # Save recording URL in session state
            #st.session_state.recording_button_clicked = True
        else:
            st.warning("No call ID found. Please make a call first.")
    except Exception as e:
        print("Error fetching call recording: ", e)
        
# Display transcript if it exists in session state
if "transcript" in st.session_state:
    if st.session_state.transcript:
        st.text_area("Transcript", st.session_state.transcript, height=300)

# Display recording if it exists in session state
if "recording" in st.session_state:
    if st.session_state.recording:
        st.audio(st.session_state.recording)
