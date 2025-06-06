# 📧 EmailGenAI - Email Generator with Intent Detection

EmailGenAI is a smart email-writing assistant that uses AI to detect your intent and generate a complete, editable email. Built with **Streamlit**, **LangGraph**, **LangChain**, and **Ollama's LLaMA 3 model**, the app allows users to quickly create formal or casual emails by simply describing what they want to write.

---

## 🔍 Features

- **Intent Detection**: Automatically identifies the purpose of the email (e.g., Request, Complaint, Thank You).
- **AI Email Drafting**: Generates emails based on user intent and description.
- **Editable Output**: Review and edit the email before sending.
- **Email Sending**: Uses Gmail SMTP integration via Yagmail to send the final email.
- **LLM-Powered Workflow**: Modular, node-based pipeline with LangGraph.

---

## 🧠 Tech Stack

- **Frontend**: Streamlit
- **LLM**: LLaMA 3 (8B via Ollama)
- **Backend Workflow**: LangGraph + LangChain
- **Email Service**: Yagmail + Gmail SMTP
- **Environment**: Python + dotenv

---



