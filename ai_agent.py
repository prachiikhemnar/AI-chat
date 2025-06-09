import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import create_react_agent

# Load environment variables
load_dotenv()

# Get API keys
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    # Select LLM provider
    if provider == "Groq":
        llm = ChatGroq(model=llm_id, api_key=GROQ_API_KEY)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id, api_key=OPENAI_API_KEY)
    else:
        return "Unsupported provider"

    # Select tools
    tools = [TavilySearchResults(api_key=TAVILY_API_KEY, max_results=2)] if allow_search else []

    # Create agent
    agent = create_react_agent(
        model=llm,
        tools=tools
    )

    # Prepare state
    state = {
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
    }

    # Invoke agent
    response = agent.invoke(state)

    # Extract AI message
    messages = response.get("messages", [])
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]

    return ai_messages[-1] if ai_messages else "No response"
