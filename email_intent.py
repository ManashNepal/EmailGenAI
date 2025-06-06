from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st

def detect_intent(state):
    user_input = state["user_input"]
    prompt = f"""
    You are an email intent detection assistant. Your task is to understand what type of email the user wants to write and output an intent phrase consisting of either a single word or exactly two words (separated by a single space), such as: Complaint, Thank You, Inquiry, Invitation, Request, Congratulations, or another appropriate intent.

    Guidelines:
    - If the user's input clearly matches one of the examples (Complaint, Thank You, Inquiry, Invitation, Request, Congratulations), use that exact phrase.
    - If not, generate a new suitable intent phrase that best represents the user's goal (e.g., Feedback, Follow Up, Recommendation, Apology).
    - Respond with ONE or TWO words only, capitalizing the first letter of each word.
    - Two-word intents must be separated by a single space; do NOT join the words together or use camel case (e.g., "Request Again", NOT "RequestAgain").
    - Do NOT include any extra text, explanation, punctuation, or quotes—only the intent phrase.

    User input:
    {user_input}

    Your response:
    """

    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content=user_input)
    ]
    response = st.session_state.llm.invoke(messages)
    state["detected_intent"] = response
    return state