import bcrypt
from db_connection import get_connection


def hash_password(plain_password):
    password_bytes = plain_password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_login(username, plain_password):
    """
    Checks username + password against Users table.
    Returns Role if login is correct.
    """
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT Password, Role FROM Users WHERE Username = ?",
            (username,)
        )
        row = cursor.fetchone()
        if row is None:
            return None

        stored_hash = row[0]
        role = row[1]

        if bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return role
        return None

    except Exception as e:
        print("Login error:", e)
        return None
    finally:
        cursor.close()
        conn.close()


def create_account(username, email, plain_password, role):
    """
    Creates a new user account.
    """
    conn = get_connection()
    if conn is None:
        return False, "Database connection failed."

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT UserID FROM Users WHERE Username = ? OR Email = ?",
            (username, email)
        )
        if cursor.fetchone():
            return False, "Username or email already exists."

        hashed_pw = hash_password(plain_password)

        cursor.execute(
            "INSERT INTO Users (Username, Email, Password, Role) VALUES (?, ?, ?, ?)",
            (username, email, hashed_pw, role)
        )
        conn.commit()
        return True, "Account created successfully."

    except Exception as e:
        return False, f"Error creating account: {e}"
    finally:
        cursor.close()
        conn.close()