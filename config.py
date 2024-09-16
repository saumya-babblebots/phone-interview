import prompts

stt_model = {
    "model": "nova-2",
    "language": "en",
    "provider": "deepgram"
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
