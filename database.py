import sqlite3
import os

def create_db():
    """ডাটাবেস এবং টেবিল তৈরি করে"""
    conn = sqlite3.connect("numbers.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, name TEXT, fb_id TEXT, points INTEGER DEFAULT 3)''')
    conn.commit()
    conn.close()
    print("✅ Database created")

def insert_user(phone, name, fb_id="Not Found", points=3):
    """নতুন ইউজার যোগ করে বা আপডেট করে"""
    try:
        conn = sqlite3.connect("numbers.db")
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO users (phone, name, fb_id, points) VALUES (?, ?, ?, ?)", 
                  (phone, name, fb_id, points))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting user: {e}")
        return False

def search_user(phone):
    """ফোন নাম্বার দিয়ে ইউজার খোঁজে"""
    try:
        conn = sqlite3.connect("numbers.db")
        c = conn.cursor()
        c.execute("SELECT name, fb_id, points FROM users WHERE phone=?", (phone,))
        result = c.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"Error searching user: {e}")
        return None

def update_points(phone, points):
    """পয়েন্ট আপডেট করে"""
    try:
        conn = sqlite3.connect("numbers.db")
        c = conn.cursor()
        c.execute("UPDATE users SET points = ? WHERE phone=?", (points, phone))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating points: {e}")
        return False

def add_sample_data():
    """নমুনা ডাটা যোগ করে"""
    sample_data = [
        ("8801974488130", "Khadiza", "Not Found", 3),
        ("8801712345678", "Rakib Hasan", "rakib.hasan.123", 3),
        ("8801812345678", "Sumaiya Akter", "sumaiya.akter", 3),
        ("8801912345678", "Tanvir Ahmed", "Not Found", 3),
        ("8801687654321", "Nusrat Jahan", "nusrat.jahan.90", 3),
        ("8801755555555", "Md Emran", "emran.hossain", 3),
        ("8801888888888", "Sadia Khan", "sadia.khan", 3),
    ]
    
    for phone, name, fb_id, points in sample_data:
        insert_user(phone, name, fb_id, points)
    
    print(f"✅ Added {len(sample_data)} sample records")

if __name__ == "__main__":
    create_db()
    add_sample_data()
    print("Database ready!")
