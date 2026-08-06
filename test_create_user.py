from authentication.auth import create_user, user_exists

username = input("Enter Username: ")
email = input("Enter Email: ")
password = input("Enter Password: ")

if user_exists(email):
    print("❌ User already exists.")
else:
    if create_user(username, email, password):
        print("✅ User created successfully!")
    else:
        print("❌ Failed to create user.")