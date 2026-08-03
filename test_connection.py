from config.db_config import get_connection

print("Testing MySQL connection...")

connection = get_connection()

if connection:
    print("✅ Connected Successfully to MySQL!")
    connection.close()
    print("🔒 Connection Closed.")
else:
    print("❌ Connection Failed.")