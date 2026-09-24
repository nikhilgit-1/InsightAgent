import os
from fastapi import FastAPI
from pydantic import BaseModel
# NAYA IMPORT: Hamne apni agent.py file se 'app_agent' ko bula liya
from agent import app_agent

# create FastAPI app
app = FastAPI()

# defien what the user will send us
class chatRequest(BaseModel):
    message: str
    
# this is the health check to verify that whether the server is running or not (GET request)
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "InsightAgent is running!"}

# this is the endpoint to handle the chat request (POST request)
@app.post("/chat")
def chat(request: chatRequest):
    
    # 1. User ke message ko Agent ki memory format (dictionary list) mein pack kiya
    initial_state = {"messages": [request.message]}
    
    # 2. Agent ko kaam par lagaya (.invoke matlab "start working")
    result = app_agent.invoke(initial_state)
    
    # 3. Agent jab poora loop ghoom kar aayega, toh uski memory mein se aakhiri reply nikal liya
    final_reply = result["messages"][-1]
    
    # 4. Debugging ke liye CMD mein print kar diya
    print(f"\n--- AGENT RESPONSE ---\n{final_reply}\n----------------------\n")
    
    # 5. Browser/Swagger UI ko jawab bhej diya
    return {"reply": final_reply}