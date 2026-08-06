import bcrypt
from config.db_config import get_connection
def hash_password(password):
    """
    Convert a plain text password into a secure hash.
    """

    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")
  #Password verification
def verify_password(password, hashed_password):
    """
    Verify whether the entered password matches the stored hash.
    """

    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
def user_exists(email):
    """
    Check whether a user with the given email already exists.
    Returns True if found, otherwise False.
    """

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    query = "SELECT id FROM users WHERE email = %s"

    cursor.execute(query, (email,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user is not None  
def create_user(username, email, password):
    """
    Create a new user in the database.
    Returns True if successful, otherwise False.
    """

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    hashed_password = hash_password(password)

    query = """
    INSERT INTO users (username, email, password_hash)
    VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(query, (username, email, hashed_password))
        connection.commit()
        return True

    except Exception as e:
        print("Error:", e)
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()  
def get_user_by_email(email):
    """
    Fetch user details using email.
    Returns user data if found, otherwise None.
    """

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT id, username, email, password_hash
    FROM users
    WHERE email = %s
    """

    cursor.execute(query, (email,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user        