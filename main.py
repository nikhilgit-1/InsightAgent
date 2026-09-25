from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import time
from agent import get_dynamic_agent
from langchain_core.messages import HumanMessage, SystemMessage # 👈 Yahan SystemMessage add kiya

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_query: str
    sql_db_url: Optional[str] = None
    nosql_uri: Optional[str] = None
    nosql_db_name: Optional[str] = None

@app.post("/api/chat")
def chat_with_db(request: ChatRequest):
    agent = get_dynamic_agent(
        sql_db_url=request.sql_db_url,
        nosql_uri=request.nosql_uri,
        nosql_db_name=request.nosql_db_name
    )

    # 👈 AI ka strict instruction ab hum yahan set kar rahe hain
    sys_msg = SystemMessage(content="""You are a smart Data Analyst AI.
    For SQL databases, write MySQL/SQLite compatible SELECT queries.
    For NoSQL databases, ALWAYS use list_nosql_collections first if you don't know the exact collection name.
    Always include the exact query you executed at the end of your response.""")

    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Agent Execution Attempt {attempt + 1}...")
            
            # 👈 Yahan SystemMessage aur User ka sawal dono ek sath ja rahe hain
            response = agent.invoke({
                "messages": [sys_msg, HumanMessage(content=request.user_query)]
            })
            
            return {"status": "success", "reply": response["messages"][-1].content}
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2) 
            else:
                return {
                    "status": "error", 
                    "reply": "Server is busy right now or API limits reached. Please try again in a moment."
                }