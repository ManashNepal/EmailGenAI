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


