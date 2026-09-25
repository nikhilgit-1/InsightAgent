import os
import json
from pymongo import MongoClient
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import certifi

load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

# FACTORY FUNCTION
def get_dynamic_agent(sql_db_url=None, nosql_uri=None, nosql_db_name=None):

    # 1. Universal SQL Tool (now this will work on any SQL database, including MySQL and SQLite)
    @tool
    def analyze_sql_database(query: str) -> str:
        """Use this tool to execute SQL queries on the connected SQL database (e.g., MySQL). Input must be a valid SQL SELECT query."""
        if not sql_db_url:
            return "Error: No SQL database is currently connected."

        if any(keyword in query.upper() for keyword in ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE"]):
            return "SECURITY ERROR: Only read-only (SELECT) operations are allowed."

        try:
            engine = create_engine(sql_db_url)
            with engine.connect() as conn:
                result = conn.execute(text(query))
                rows = result.fetchall()
                if not rows:
                    return "No data found."
                # Data ko clean list format mein bhej rahe hain
                return str([tuple(row) for row in rows])
        except Exception as e:
            return f"SQL Error: {str(e)}"

    # 2. NoSQL Table Finder Tool (now ai will first find the collection name before querying)
    @tool
    def list_nosql_collections() -> str:
        """Use this tool FIRST to get a list of all available collections (tables) in the NoSQL database."""
        if not nosql_uri or not nosql_db_name:
            return "Error: NoSQL database is not fully connected."
        try:
            client = MongoClient(nosql_uri, tls=True, tlsCAFile=certifi.where())
            db = client[nosql_db_name]
            collections = db.list_collection_names()
            client.close()
            return f"Available collections in NoSQL: {', '.join(collections)}"
        except Exception as e:
            return f"Error listing collections: {str(e)}"

    # 3. NoSQL Query Tool (now ai will query the specific collection)
    @tool
    def analyze_nosql_database(collection_name: str, query_json: str) -> str:
        """
        Use this tool to search a specific NoSQL collection.
        Input needs the 'collection_name' and a valid JSON string 'query_json'.
        """
        if not nosql_uri or not nosql_db_name:
            return "Error: NoSQL database is missing."
        try:
            filter_query = json.loads(query_json)
            client = MongoClient(nosql_uri, tls=True, tlsCAFile=certifi.where())
            db = client[nosql_db_name]
            collection = db[collection_name]
            results = list(collection.find(filter_query, {"_id": 0}))
            client.close()
            return json.dumps(results, indent=2) if results else "No data found."
        except Exception as e:
            return f"NoSQL Error: {str(e)}"

    tools = [analyze_sql_database, list_nosql_collections, analyze_nosql_database]

    system_message = """You are a smart Data Analyst AI.
    For SQL databases, write MySQL/SQLite compatible SELECT queries.
    For NoSQL databases, ALWAYS use list_nosql_collections first if you don't know the exact collection name.
    Always include the exact query you executed at the end of your response."""
    
    # agent.py ki AAKHIRI line ko isse replace kar do
    return create_react_agent(llm, tools)