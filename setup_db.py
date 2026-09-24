import sqlite3

# 1. Database Connection: Yeh line ek nayi file 'business_data.db' banayegi (agar nahi hai toh)
conn = sqlite3.connect("business_data.db")
cursor = conn.cursor()

# 2. Table Creation: Ek 'sales' naam ki table banayenge jisme id, product, revenue, region, aur month honge
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    revenue INTEGER,
    region TEXT,
    month TEXT
)
""")

# 3. Clean and Insert: Purana kachra saaf karke naya dummy data daalenge
cursor.execute("DELETE FROM sales")
sample_data = [
    ('Laptop', 120000, 'Jaipur', 'January'),
    ('Smartphone', 85000, 'Jaipur', 'January'),
    ('Laptop', 95000, 'Delhi', 'February'),
    ('Tablet', 30000, 'Mumbai', 'February')
]
cursor.executemany("INSERT INTO sales (product, revenue, region, month) VALUES (?, ?, ?, ?)", sample_data)

# 4. Save and Close: Data save karke connection band kar denge
conn.commit()
conn.close()

print("Database 'business_data.db' created successfully with sample sales data!")