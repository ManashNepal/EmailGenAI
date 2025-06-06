import streamlit as st
import os
from dotenv import load_dotenv
from langchain_ollama.llms import OllamaLLM

from email_flow import graph
from utils import parse_subject, parse_body
from email_sender import send_email

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

st.set_page_config(page_title="EmailGenAI", page_icon=":envelope_with_arrow:")

st.header("Email Generator with Intent Detection :mailbox_with_mail:")
user_prompt = st.text_input(label="Describe the email you want to generate: ")

if "llm" not in st.session_state:
    st.session_state.llm = OllamaLLM(model="llama3:8b")

if st.button("Generate", key="generate_button") and user_prompt:
    with st.spinner("Generating"):
        state = {
            "user_input": user_prompt
        }
        result = graph.invoke(state)
        st.session_state.detected_intent = result["detected_intent"]
        st.session_state.generated_email = result["generated_email"]

if "generated_email" in st.session_state:
    email_subject = parse_subject(st.session_state.generated_email)
    email_body = parse_body(st.session_state.generated_email)

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
                send_email(
                    EMAIL_ADDRESS,
                    EMAIL_APP_PASSWORD,
                    recipient_mail,
                    email_subject,
                    edited_email,
                )
                st.success("Email Sent Successfully!")
            except Exception as e:
                st.warning(f"Unable To Send Mail: {e}!")
