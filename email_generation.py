from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st

def generate_email(state):
    detected_intent = state["detected_intent"].strip().lower()
    user_input = state["user_input"]
    formal_intents = ["complaint", "inquiry", "request"]
    friendly_intents = ["thank you", "invitation", "congratulations"]

    if detected_intent in formal_intents:
        tone = "formal"
    elif detected_intent in friendly_intents:
        tone = "friendly and warm"
    else:
        tone = "neutral"

    prompt = f"""
    You are an expert email assistant. Write a well-structured email based on the following intent and description.

    Intent: {detected_intent.capitalize()}
    Description: {user_input}

    Instructions:
    - Use a {tone} tone.
    - Include a subject line that summarizes the email.
    - Start with a greeting (e.g., Dear [Recipient],).
    - End with an appropriate closing such as 'Best regards' or 'Yours sincerely'.
    - Add a line break after the closing, then write [Your Name] on the next line.
    - Make sure to use correct spacing and punctuation.
    - Do NOT include the phrase 'Intent:' or 'Description:' in the final email.
    - Your response should start exactly with: 'Here is a draft email based on your prompt:'

    Example:

    Intent: Thank you
    Description: Thank the customer for their purchase.

    Here is a draft email based on your prompt:
    Subject: Thank You for Your Purchase

    Dear Customer,

    Thank you very much for your recent purchase. We appreciate your business.

    Best regards,\n
    [Your Name]

    Now, please generate the email below:
    """
    
    messages = [
        SystemMessage(content = prompt),
        HumanMessage(f"Intent: {detected_intent} \n Description : {state['user_input']}")
    ]
    response = st.session_state.llm.invoke(messages)
    state["generated_email"] = response
    return state