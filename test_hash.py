from authentication.auth import hash_password

password = "Dnyanu@123"

hashed = hash_password(password)

print("Original Password :", password)
print("Hashed Password   :", hashed)