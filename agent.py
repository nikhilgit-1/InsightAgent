import os
import time
from google import genai
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

# 1. Initialize environment variables and the generative AI client
load_dotenv()
client = genai.Client()

# 2. Define the Agent's State (Memory)
# 'add_messages' ensures new messages are appended to the conversation history rather than overwriting it.
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Define the LLM Node (The core processing function)
def call_llm(state: AgentState):
    # Extract the most recent message from the state
    last_message = state["messages"][-1]
    
    # Implement a retry mechanism to handle temporary 503 Server Unavailable errors
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Attempt to generate content using the reliable free-tier model
            response = client.models.generate_content(
                model="gemini-3.6-flash", 
                contents=last_message.content
            )
            # Return the successful response to append to the state
            return {"messages": [response.text]}
        
        except Exception as e:
            # Log the retry attempt to the console if the server is overwhelmed
            print(f"\n[SYSTEM WARNING] API server overload encountered (Attempt {attempt + 1}/{max_retries}). Retrying in 5 seconds...\n")
            time.sleep(5)
            
        # Graceful fallback response if all retry attempts fail
    return {"messages": ["System Notice: The AI service is currently experiencing exceptionally high traffic. Please try your request again in a few moments."]}
   
    # Return the model's response to be appended to the state
    return {"messages": [response.text]}

# 4. Construct the StateGraph (The workflow/routing logic)
workflow = StateGraph(AgentState)

# Add the primary processing node
workflow.add_node("bot", call_llm)

# Define the execution edges: Start -> Bot -> End
workflow.add_edge(START, "bot")
workflow.add_edge("bot", END)

# Compile the graph into an executable agent application
app_agent = workflow.compile()