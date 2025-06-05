# Email Generator With Intent Detection
from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st

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
    messages = [
        SystemMessage(content="Extract the intent only. Some of the examples of intent are: complaint, thank you, inquiry, invitation. Respond only with the intent word which may not be listed in the example too."),
        HumanMessage(content=user_input)
    ]
    response = st.session_state.llm.invoke(messages)
    state["detected_intent"] = response
    return state 

def generate_email(state):
    detected_intent = state["detected_intent"]
    messages = [
        SystemMessage(content = """
        Write an email using the given intent and description.
        Include a subject, greeting, body, and a suitable closing like 'Best regards' or 'Yours sincerely'.                  
        Add a line break after the closing, then write [Your Name] on the next line.
        Keep the email clear and well-formatted. Make it short or detailed as needed. 
        Start your reply with: 'Here is a draft email based on your prompt:'
        """),
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


