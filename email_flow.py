from langgraph.graph import StateGraph
from langchain_core.runnables import RunnableLambda
from email_intent import detect_intent
from email_generation import generate_email
from typing import TypedDict, Optional

class MyState(TypedDict):
    user_input : Optional[str]
    detected_intent : Optional[str]
    generated_email : Optional[str]

def start_node(state):
    return state

def end_node(state):
    return state

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
