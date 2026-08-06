from authentication.auth import hash_password, verify_password

password = "Dnyanu@123"

hashed_password = hash_password(password)

print("Original Password :", password)
print("Hashed Password   :", hashed_password)

if verify_password("Dnyanu@123", hashed_password):
    print("✅ Correct password verified!")
else:
    print("❌ Correct password verification failed!")

if verify_password("WrongPassword", hashed_password):
    print("❌ Wrong password incorrectly verified!")
else:
    print("✅ Wrong password rejected!")