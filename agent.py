import os
import json
from pymongo import MongoClient
import sqlite3
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import certifi

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
    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
    ]
    upper_query = query.upper()

    # Agar AI ne koi aisi query banayi jisme yeh forbidden words hain, toh error de do
    if any(keyword in upper_query for keyword in forbidden_keywords):
        return "SECURITY ERROR: You are strictly restricted to read-only (SELECT) operations. Modification is blocked."

    # 3. Execution Layer: Agar query safe (SELECT) hai, toh use database par chalao
    try:
        conn = sqlite3.connect("business_data.db")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()  # Data nikal lo
        conn.close()

        if not results:
            return "No data found for this query."
        return str(
            results
        )  # Raw data AI ko wapas bhej do taaki wo English mein answer bana sake
    except Exception as e:
        return f"SQL Error: {str(e)}"


@tool
def analyze_nosql_database(query_json: str) -> str:
    """
    Use this tool to search the NoSQL database for unstructured data like customer support tickets.
    The input MUST be a valid JSON string representing a MongoDB filter.
    Examples of input:
    - '{"status": "Open"}'
    - '{"priority": "High"}'
    - '{"tags": "finance"}'
    """
    try:
        # AI se aayi hui JSON string ko Python dictionary mein convert karna
        filter_query = json.loads(query_json)
        print(f"\n[SYSTEM ALERT] 🔍 Executing NoSQL Query: {query_json}\n")

        # MongoDB se connection banana
        mongo_uri = os.getenv("MONGODB_URI")
        client = MongoClient(
            mongo_uri,
            tls=True,
            tlsCAFile=certifi.where()
        )
        
        db = client["business_data_nosql"]
        collection = db["support_tickets"]

        # Database mein search karna (_id: 0 ka matlab hai default complex ID ko hide karna)
        results = list(collection.find(filter_query, {"_id": 0}))
        client.close()

        if not results:
            return "No data found matching your query."

        return json.dumps(results, indent=2)

    except json.JSONDecodeError:
        return "Error: Agent provided an invalid JSON format."
    except Exception as e:
        return f"Error executing NoSQL query: {str(e)}"


# 4. Initialize Engine: LLM ko define kiya
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

# 5. Compile Agent: LLM aur uske tool (hathyar) ko jod kar ek ReAct Agent bana diya
tools = [analyze_sql_database, analyze_nosql_database]

# (System Message)
system_message = """You are a smart Data Analyst AI.
Your job is to answer user questions by querying the connected databases.
Whenever you use the SQL or NoSQL tool to fetch data, you MUST include the exact query you executed at the end of your final response, formatted as a code block.
"""

# state_modifier ke through hum AI ko uske rules batate hain = we change the code beacuse it was creating a dependency hell

app_agent = create_react_agent(llm, tools)
