# Email Generator with Intent Detection

An interactive Streamlit app that uses LangGraph and Ollama LLM to detect the intent from user input and generate a well-structured email draft accordingly.

---

## Features

- Detects user intent from a natural language description (e.g., complaint, thank you, inquiry, invitation, etc.)
- Generates a clear, concise, and well-formatted email based on the detected intent and user description.
- Uses OpenAI-style prompt engineering with Ollama LLM (`llama3:8b` model).
- Implements a state graph workflow with LangGraph for modular and maintainable code.
- Easy to use, interactive web interface built with Streamlit.