import os
from dotenv import load_dotenv
from pymongo import MongoClient

# 1. Environment variables (password wali file) load karo
load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")

# 2. Cloud Database se Connection Banao
# MongoClient wo tool hai jo internet ke through MongoDB tak data le jata hai
client = MongoClient(mongo_uri)

# 3. Database aur Collection (Table) define karo
# SQL mein hum 'Database' aur 'Table' bolte hain. 
# NoSQL mein hum 'Database' aur 'Collection' bolte hain.
db = client["business_data_nosql"]
collection = db["support_tickets"]

# 4. Purana kachra saaf karo (agar pehle se data hai toh delete kar do)
collection.delete_many({})

# 5. Dummy Unstructured Data (Notice karo ki sabka format thoda alag hai)
# SQL mein aisa flexible data nahi daal sakte, error aa jata.
sample_tickets = [
    {
        "ticket_id": "T-101", 
        "customer": "Rahul", 
        "issue": "Laptop screen flickering", 
        "status": "Open", 
        "priority": "High"
    },
    {
        "ticket_id": "T-102", 
        "customer": "Sneha", 
        "issue": "Payment failed but money deducted", 
        "status": "Closed", 
        "tags": ["finance", "urgent"] # Dekho isme naya format (List/Array) ghusa diya
    },
    {
        "ticket_id": "T-103", 
        "customer": "Amit", 
        "issue": "How to change password?", 
        "status": "Open", 
        "rating": 4 # Isme rating daal di
    }
]

# 6. Data ko cloud par insert karo
collection.insert_many(sample_tickets)
print("NoSQL Database populated successfully on MongoDB Atlas!")

# Connection band karo
client.close()