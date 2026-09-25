from fastapi import FastAPI
from pydantic import BaseModel
from agent import app_agent, system_message # Hamne agent.py se apna banaya hua app_agent yahan import kar liya

app = FastAPI()

# 1. Pydantic Model: Yeh ensure karta hai ki user jo data bhej raha hai, usme 'message' naam ki string zaroor ho
class chatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: chatRequest):
    # 2. Format Input: User ke message ko LangGraph ke samajh aane wale format mein set kiya
    initial_state = {
        "messages": [
            ("system", system_message),
            ("user", request.message)
        ]
    }
    
    # 3. Agent Execution: Agent ko start kiya (invoke)
    result = app_agent.invoke(initial_state)
    
    # 4. Extract Reply: Agent ki poori thinking process se sirf aakhiri final answer nikala
    raw_reply = result["messages"][-1].content
    
    # 5. Output Cleaning: LangChain kabhi-kabhi extra metadata bhejta hai, use saaf karke pure text banaya
    if isinstance(raw_reply, list):
        final_reply = raw_reply[0].get("text", str(raw_reply))
    else:
        final_reply = str(raw_reply)
        
    # 6. Return Response: Frontend/Swagger UI ko final saaf answer bhej diya
    return {"reply": final_reply}