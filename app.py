# Email Generator With Intent Detection
from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st
import yagmail
from dotenv import load_dotenv
import os
import re

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

st.set_page_config(page_title="EmailGenAI", page_icon=":envelope_with_arrow:")

st.header("Email Generator with Intent Detection :mailbox_with_mail:")
user_prompt = st.text_input(label="Describe the email you want to generate: ")

if "llm" not in st.session_state:
    st.session_state.llm = OllamaLLM(model="llama3:8b")

class MyState(TypedDict):
    user_input : Optional[str]
    detected_intent : Optional[str]
    generated_email : Optional[str]


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
    

def start_node(state):
    return state

def end_node(state):
    return state
    
    
# Creating Nodes

builder = StateGraph(state_schema=MyState)

builder.add_node("start", RunnableLambda(start_node))
builder.add_node("intent_detection", RunnableLambda(detect_intent))
builder.add_node("email_generation", RunnableLambda(generate_email))
builder.add_node("end", RunnableLambda(end_node))

builder.add_edge("start", "intent_detection")
builder.add_edge("intent_detection", "email_generation")
builder.add_edge("email_generation", "end")

builder.set_entry_point("start")
builder.set_finish_point("end")

graph = builder.compile()


if st.button("Generate", key = "generate_button") and user_prompt:
    with st.spinner("Generating"):
        state = {
            "user_input" : user_prompt
        }       
        result = graph.invoke(state)
        st.session_state.detected_intent = result["detected_intent"]
        st.session_state.generated_email = result["generated_email"]

if "generated_email" in st.session_state:
    subject_match = re.search(r"Subject:\s*(.+)", st.session_state.generated_email)
    email_subject = subject_match.group(1).strip() if subject_match else ""

    body_match = re.search(r"(Dear\s.+)", st.session_state.generated_email, re.DOTALL)
    email_body = body_match.group(1).strip() if body_match else ""
    st.subheader("Detected Intent")
    st.write(st.session_state.detected_intent)
    st.subheader("Edit The Generated Email:")
    edited_email = st.text_area(
        "Edit the email before sending",
        value=email_body,
        height=500,
        key="editable_email_area"
        )
    st.session_state.editable_email = edited_email
    recipient_mail = st.text_input("Enter the recipient mail: ")
    if st.button("Send Mail", key="send_button"):
        with st.spinner("Sending"):
            try:
                
                yag = yagmail.SMTP(user="manash.nepal111@gmail.com", password="gaml afjo zege mgtf")
                yag.send(
                    to=recipient_mail, 
                    subject=email_subject, 
                    contents=edited_email)
                st.success("Email Sent Successfully!")
            except Exception  as e:
                st.warning(f"Unable To Send Mail : {e}!")
            
        # st.download_button(label="Download Email", file_name="generated_email.txt", data = result["generated_email"].replace("Here is a draft email based on your prompt:\n\n", ""))


