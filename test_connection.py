from config.db_config import get_connection

print("Testing PostgreSQL connection...")

connection = get_connection()

if connection:
    print("✅ Connected Successfully to PostgreSQL!")
    connection.close()
    print("🔒 Connection Closed.")
else:
    print("❌ Connection Failed.")