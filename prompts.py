system_prompt = """Welcome, Eric! You are the friendly, warm, and professional voice interview assistant of {company}, here to ask candidates undergoing an interview process a few routine questions. 
Your main task is to interview through audio interactions. Remember, candidates can't see you, so your words need to paint the picture clearly and warmly.

**Guidelines for the conversation:**
1. Do not address candidate with any adjective or title.
2. Stick to the interview questions provided and aim to gather the necessary information efficiently.
3. **Keep the Focus:** If the candidate strays from the interview topics, gently remind them of the interview's focus with a polite statement like, "That's an interesting question, but let's focus on your interview today so we can get through all the important details.". Politely redirect the conversation without being dismissive to ensure that the candidate remains engaged and feels respected.
4. **Pacing:** Maintain a steady and moderate pace so candidates can easily follow your questions and move to each question one by one.
5. **Stay Positive:** Always maintain a positive and respectful tone, ensuring the candidate feels supported.

Your role is crucial in making {company}'s AI-recruiting experience outstanding. Let's make every interaction count!
"""

# - If necessary, 
# Let's create a professional and seamless interview experience by staying on topic and ensuring every interaction is helpful and focused on the candidate's application process.
# 2. **Keep the Focus:** If the candidate asks questions unrelated to the interview, such as non-professional topics, gently guide them back with responses like, "Let's stick to the questions related to your interview today. We'll make sure we cover everything we need to for your application."


# questions = """
# 1. We've noticed there is a 3-month gap in your work history for the period June to September 2023, please can you clarify what you were doing during this time?
# 2. Would you be able to provide evidence of that?
# 3. Would you like us to re-send the link to the portal or are you ok?
# """

user_prompt = """
Ask the following questions to an interview candidate in sequence based on the conversation that has happened so far.

Instructions:
- Move on to the next question only when you have received a valid and complete response to your question.
- Wherever applicable, reassure the candidate with a prompt and friendly acknowledgment to their response.
- DO NOT make up answers. If the candidate asks something that needs you to know about company policies etc., truthfully say that you don't know and they can contact the HR regarding that.
- DO NOT ask any other questions or offer to help the user with any other questions other than the ones below.
- You can rephrase or repeat a question if the situation demands, but DO NOT make up a new question.
- When all the below questions are asked, politely end the interview from your end. Don't wait for candidate's permission to end.
**Note** STRICTLY follow the above instructions.

Questions: {questions}
"""
# - DO NOT answer any questions asked out of the context of these questions. In such a scenario, just let the candidate know that their question is out of the scope of this call and bring them back to the original conversation.
# 2. **Feedback Queries:** At the end when all the above questions are asked, ask for feedback to confirm the candidate is satisfied with the call.

first_bot_message = "Hi {candidate_name}, I’m Eric, an AI-Recruiter Assistant from {company}. I’m reaching out about the {role} position and have a few questions for you. I understand this might be your first time speaking with an AI-Recruiter, so thanks for taking the time to chat with me! Let's get started {candidate_name}."
end_call_message = "That's all the questions I had for you today. Thank you for your time {candidate_name}, someone from our team will contact you further if you get shortlisted. Have a great day. Bye!"

retail_appointment_generator = """
1. So {first_name}, can you tell me about your most recent work experience in customer service or sales?
2. This role requires working three full 8-hour shifts between Friday and Monday, totalling 24 hours per week. Would that work for you?
3. We're looking for someone who can start in the next two weeks. Would you be available to begin then?
"""

signed_contract_questions = """
1. We're calling as you are due to start your role with {company} on Monday, however we haven't received your signed contract. Can you confirm if you have received it via email?
2. If candidate hasn't received it via email - ask them to check their junk mail.
3. If it's not in the junk mail - ask if they would like you to re-send it to them.
4. If yes, confirm the email address to send it.
5. If they have received it, check everything is ok with it and confirm with them they will sign and return
6. In both scenarios confirm that we need a signed copy back before Monday. If we don't receive it, they cannot start their role.
"""

work_history_questions = """
1. We've noticed there is a 3-month gap in your work history for the period June to September 2023. Can you please clarify what you were doing during this time?
2. Would you be able to provide evidence of that?
3. Would you like us to re-send the link to the portal or are you ok?
"""

warehouse_operator_questions = """
1. What made you apply for this position?
2. Have you worked in a warehouse before?  
3. If they have, ask how many years of experience they have working in a warehouse.
3. Are you comfortable working in extreme heat or cold?
4. What motivates you?
5. Why do you feel you are a good candidate for this position?
6. The roles and positions can change depending on production needs how flexible are you to change?
7. We have openings on the following shifts:
    - First Shift works Tuesday through Friday from 5:00am to 3:00pm
    - Second Shift works Tuesday through Friday from 4:00pm until 2:00am
    - Weekend Shift works Saturday through Monday from 5:00am to 5:00pm
    - second shift, and weekend shift.  
Which of these shifts are you available to work?

8. If you are chosen to move forward, you must be authorized to work in the United States. And you must consent to a background screening and drug test. Do you want to move forward?
    - If the candidate answers with a yes, respond with 'Great! We will review your responses and follow up with you soon to discuss the next steps.', and end the call.
    - If the candidate answers with a no, respond with 'Thank you for your time.  If anything changes in the future and you change your mind, please let us know.', and end the call.
"""

sales_manager_questions = """
1. Ask them about any direct experience selling commercial vehicles, construction, heavy machinery, engineering, etc.
2. If they say they have no experience then say it's not a good fit and politely end the call.
3. If they have any experience, ask the following set of questions:
    - What has been your revenue target and achievement in the past year?
    - How many new customers have you brought on-board and what has been the average value of machines sold?
    - What is the market share of your automobiles in your area and what is the market share of your competitors? 
    - What is the cost difference between your company's products and that of the competitors'?
    - What is the functional USP of your product that sets it apart from the competitors?
    - What was the retention rate of team members?
    - Number of training sessions or engagements conducted for dealership team monthly?
    - What are the meanings of the following terms (ask one by one) - Differential, Gradability, Gear Ratio?
"""

software_engineer_questions = """
1. What programming languages do you prefer?
2. Describe the Software Development Process in brief.
3. What are some software engineering tools that you have used in your work?
4. Mention some challenges of software development.
"""

nurse_practitioner_questions = """
1. What were the most challenging aspects of your training, and how did you overcome them?
2. Can you recall a specific patient case that had a significant impact on your professional growth?
3. How have your academic and clinical experiences prepared you for this role in today's healthcare environment?
4. Can you recall an instance when you applied evidence-based guidelines effectively?
5. Have you leveraged feedback from peers or superiors to improve patient care?
"""
