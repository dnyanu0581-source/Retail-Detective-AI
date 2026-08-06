from authentication.auth import user_exists

email = input("Enter email to check: ")

if user_exists(email):
    print("✅ User already exists.")
else:
    print("❌ User not found.")