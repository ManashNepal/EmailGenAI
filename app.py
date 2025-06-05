# Email Generator With Intent Detection
from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st
from IPython.display import Image, display

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
    You are an email intent detection assistant. Your task is to understand what type of email the user wants to write and output a ** single or two word intent** word like: Complaint, Thank You, Inquiry, Invitation, Request, Congratulations, or a new one if needed.

    Guidelines:
    - If the user's input clearly matches one of the examples (Complaint, Thank You, Inquiry, Invitation, Request, Congratulations), use it.
    - If not, **generate a new suitable intent** that best represents the user's goal (e.g., "Feedback", "Follow-Up", "Recommendation", "Apology").
    - **Respond with a SINGLE word or TWO words if necessary** with first letter capitalized. No extra text or punctuation.

    User input:
    \"\"\"{user_input}\"\"\"

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


if st.button("Generate") and user_prompt:
    with st.spinner("Generating"):
        state = {
            "user_input" : user_prompt
        }       
        result = graph.invoke(state)
        st.subheader("Detected Intent")
        st.write(result["detected_intent"])
        st.subheader("Generated Email")
        st.write(result["generated_email"])

        st.download_button(label="Download Email", file_name="generated_email.txt", data = result["generated_email"].replace("Here is a draft email based on your prompt:\n\n", ""))


