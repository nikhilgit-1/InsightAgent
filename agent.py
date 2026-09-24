import os
import sqlite3
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

# 1. The Secure Database Tool
# @tool LangChain ko batata hai ki yeh function AI use kar sakta hai
@tool
def analyze_sql_database(query: str) -> str:
    """
    Use this tool to execute SQL queries on the 'business_data.db' database.
    The database has a table named 'sales' with columns: id, product, revenue, region, month.
    Input must be a valid SQL SELECT query.
    """
    print(f"\n[SYSTEM ALERT] 🔍 Executing SQL Query: {query}\n")
    
    # 2. SECURITY LAYER: Strict keyword blocking
    forbidden_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'TRUNCATE', 'CREATE']
    upper_query = query.upper()
    
    # Agar AI ne koi aisi query banayi jisme yeh forbidden words hain, toh error de do
    if any(keyword in upper_query for keyword in forbidden_keywords):
        return "SECURITY ERROR: You are strictly restricted to read-only (SELECT) operations. Modification is blocked."

    # 3. Execution Layer: Agar query safe (SELECT) hai, toh use database par chalao
    try:
        conn = sqlite3.connect("business_data.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall() # Data nikal lo
        conn.close()
        
        if not results:
            return "No data found for this query."
        return str(results) # Raw data AI ko wapas bhej do taaki wo English mein answer bana sake
    except Exception as e:
        return f"SQL Error: {str(e)}"

# 4. Initialize Engine: LLM ko define kiya
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

# 5. Compile Agent: LLM aur uske tool (hathyar) ko jod kar ek ReAct Agent bana diya
tools = [analyze_sql_database]
app_agent = create_react_agent(llm, tools)