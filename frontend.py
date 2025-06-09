import streamlit as st
import requests

# Set up Streamlit page
st.set_page_config(page_title="LangGraph Agent UI", layout="wide")
st.title("AI Chatbot Agents")
st.write("Create and interact with the AI Agents!")

# System prompt input
system_prompt = st.text_area(
    "Define your AI Agent:", height=70, placeholder="Type your system prompt here..."
)

# Model options
MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

# Provider selection
provider = st.radio("Select provider:", ("Groq", "OpenAI"))

# Model selection based on provider
if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

# Allow web search
allow_web_search = st.checkbox("Allow web search")

# User query
user_query = st.text_area("Enter your query:", height=150, placeholder="Ask anything...")

# Backend API URL (adjust as needed)
API_URL = "http://127.0.0.1:9999/CHAT"  # Or your machine IP if accessed from other devices

# Submit button
if st.button("Ask Agent"):
    if user_query.strip():
        # Prepare payload
        payload = {
            "model_name": selected_model,
            "provider": provider,
            "llm_id": selected_model,
            "allow_search": allow_web_search,
            "system_prompt": system_prompt,
            "query": user_query
        }

        try:
            # Make POST request to backend
            res = requests.post(API_URL, json=payload)
            res.raise_for_status()  # Raise an exception for HTTP errors
            response = res.json().get("response", "No response from agent.")
        except Exception as e:
            response = f"API request failed: {e}"

        # Display response
        st.subheader("Agent response")
        st.markdown(f"**Final response:** {response}")
    else:
        st.warning("Please enter a query before asking.")
