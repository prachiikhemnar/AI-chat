from fastapi import FastAPI
from pydantic import BaseModel
from ai_agent import get_response_from_ai_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request body schema
class RequestState(BaseModel):
    query: str
    provider: str
    llm_id: str
    allow_search: bool
    system_prompt: str

# Endpoint for chatbot interaction
@app.post("/chat")
def chat_with_agent(request: RequestState):
    response = get_response_from_ai_agent(
        llm_id=request.llm_id,
        query=request.query,
        allow_search=request.allow_search,
        system_prompt=request.system_prompt,
        provider=request.provider
    )
    return {"response": response}

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)
