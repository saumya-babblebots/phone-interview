# import requests
# #from dotenv import load_dotenv
# #import os
# import streamlit as st
# from app import get_call_id

# st.markdown("# Interview Recording")  
# st.sidebar.markdown("# Get Recording")  

# st.markdown("<br><br>", unsafe_allow_html=True)

# auth_token = st.secrets["auth_token"]
# #call_id = '5f2427fa-7237-4791-9533-d25e84f5f171'

# call_id = get_call_id()

# if st.button("Call Recording"):
#     st.markdown("<br>", unsafe_allow_html=True)
#     if call_id:
            
#         url = f"https://api.vapi.ai/call/{call_id}"

#         headers = {
#             'Authorization': f'Bearer {auth_token}',
#             'Content-Type': 'application/json',
#         }

#         response = requests.request("GET", url, headers=headers)
#         recording = response.json().get("recordingUrl",None)
#         print(recording)
        
#         if recording:
#             st.markdown("<br><br>", unsafe_allow_html=True)
#             st.audio(recording)
#         else:
#             st.error("No recording found")
        
#     else:
#         st.error("Call id not found, please make a call first")
