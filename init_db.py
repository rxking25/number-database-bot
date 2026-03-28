from database import create_db, add_sample_data

if __name__ == "__main__":
    create_db()
    add_sample_data()
    print("✅ Database initialized successfully!")
