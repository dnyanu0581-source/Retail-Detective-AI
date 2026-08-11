import bcrypt

from config.db_config import get_connection


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Convert a plain-text password into a secure bcrypt hash.
    """

    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


# ============================================================
# PASSWORD VERIFICATION
# ============================================================

def verify_password(password, hashed_password):
    """
    Verify whether the entered password matches
    the stored bcrypt password hash.

    Returns:
        True  -> password matches
        False -> password does not match
    """

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )

    except (ValueError, TypeError):
        return False


# ============================================================
# CHECK USER EXISTS
# ============================================================

def user_exists(email):
    """
    Check whether a user with the given email already exists.

    Returns:
        True  -> user exists
        False -> user does not exist or database error
    """

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        query = """
            SELECT id
            FROM users
            WHERE email = %s
        """

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        return user is not None

    except Exception as e:
        print(f"User existence check error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


# ============================================================
# CREATE USER
# ============================================================

def create_user(username, email, password):
    """
    Create a new user in the PostgreSQL users table.

    Returns:
        True  -> user created successfully
        False -> creation failed
    """

    connection = get_connection()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        # Hash password before storing it
        hashed_password = hash_password(password)

        query = """
            INSERT INTO users (
                username,
                email,
                password_hash
            )
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                username,
                email,
                hashed_password
            )
        )

        connection.commit()

        return True

    except Exception as e:
        print(f"User creation error: {e}")

        connection.rollback()

        return False

    finally:
        cursor.close()
        connection.close()


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(email):
    """
    Fetch user information using their email.

    Returns:
        Dictionary containing user information
        if the user exists.

        None if the user does not exist
        or a database error occurs.
    """

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor()

    try:
        query = """
            SELECT
                   id,
                   username,
                   email,
                   password_hash
                   FROM users
                   WHERE email = %s
        """

        cursor.execute(query, (email,))

        row = cursor.fetchone()

        if row is None:
            return None

        # Convert PostgreSQL tuple into dictionary
        user = {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
            
        }

        return user

    except Exception as e:
        print(f"User fetch error: {e}")

        return None

    finally:
        cursor.close()
        connection.close()