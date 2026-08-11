from authentication.auth import (
    create_user,
    user_exists,
    get_user_by_email,
    verify_password
)


email = "test@example.com"
username = "Test User"
password = "TestPassword123"


print("\n========== AUTHENTICATION TEST ==========\n")


# 1. Check whether user exists
print("1️⃣ Checking whether user exists...")

if user_exists(email):
    print("⚠️ User already exists.")
else:
    print("✅ User does not exist yet.")


# 2. Create user
if not user_exists(email):

    print("\n2️⃣ Creating user...")

    result = create_user(
        username,
        email,
        password
    )

    if result:
        print("✅ User created successfully!")
    else:
        print("❌ User creation failed.")


# 3. Fetch user
print("\n3️⃣ Fetching user...")

user = get_user_by_email(email)

if user:
    print("✅ User found!")
    print("Username:", user["username"])
    print("Email:", user["email"])
else:
    print("❌ User not found.")


# 4. Verify password
if user:

    print("\n4️⃣ Checking password...")

    password_correct = verify_password(
        password,
        user["password_hash"]
    )

    if password_correct:
        print("✅ Password verification successful!")
    else:
        print("❌ Password verification failed.")


print("\n========== TEST COMPLETE ==========\n")