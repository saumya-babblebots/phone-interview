import prompts

stt_model = {
    "model": "nova-2",
    "language": "en",
    "provider": "deepgram",
    "keywords": []
}

llm = {
    "provider": "openai",
    "model": "gpt-4o-mini",
    "maxTokens": 150,
    "messages": [
        {
            "role": "system",
            "content": prompts.system_prompt #.format(company=company),
        }, 
        {
            "role": "assistant",
            "content": prompts.user_prompt
        }
    ]
}

REGION_VOICES = {
    "US": {
        "model": "eleven_turbo_v2_5",
        "voiceId": "cjVigY5qzO86Huf0OWal",  
        "provider": "11labs",
        "stability": 0.5,
        "similarityBoost": 0.75
    },
    "India": {
                    "model": "eleven_multilingual_v2",
                    "style": 0.1,
                    "voiceId": "3gsg3cxXyFLcGIfNbM6C",
                    "provider": "11labs",
                    "stability": 0.5,
                    "similarityBoost": 0.75
    }
}

def get_assistant(selected_template: str, region: str, company: str, candidate_name: str, role: str, questions: str):
    recruiter = "Eric"
    if region == 'India':
        recruiter = "Tushar"        
    
    first_bot_message = prompts.alt_first_bot_message.format(candidate_name=candidate_name)
    if company.isalpha():
        stt_model["keywords"].append(company)
    
    if candidate_name.isalpha():
        stt_model["keywords"].append(candidate_name)
    
    print(stt_model["keywords"])
    llm["messages"][0]["content"] = prompts.system_prompt.format(company=company)

    if (selected_template == "Structural Coatings - Material Handler") or (
        selected_template == "Hurricane Clean-Up Labor"
    ):
        llm['messages'][1]['content'] = prompts.user_prompt_material_handler.format(
            recruiter=recruiter,
            questions=questions, 
            company=company,
            role=role,
        )
    else:
        llm['messages'][1]['content'] = prompts.user_prompt_with_probing.format(
            questions=questions, 
            company=company, 
            role=role, 
            recruiter=recruiter
        )
    
        
    voice_settings = REGION_VOICES.get(region, REGION_VOICES['US'])

    vapi_assistant = {
        "firstMessage": first_bot_message,
        #"endCallMessage": prompts.end_call_message.format(candidate_name=candidate_name),
        "endCallPhrases": ["Have a great day."],
        "backgroundDenoisingEnabled": True,
        "responseDelaySeconds": 1.0,
        "silenceTimeoutSeconds": 30,
        "transcriber": stt_model,
        "model": llm,
        "startSpeakingPlan": {
            "waitSeconds": 1.0
        },
        "endCallFunctionEnabled": True,
        "voice": voice_settings,
        "backgroundSound": "off"
    }

    return vapi_assistant
