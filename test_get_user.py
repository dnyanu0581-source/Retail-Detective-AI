from authentication.auth import get_user_by_email

email = input("Enter email: ")

user = get_user_by_email(email)

if user:
    print("User Found")
    print(user)
else:
    print("User Not Found")