import bcrypt
from db_connection import get_connection

def verify_login(username, plain_password):
    """
    Checks username + password against the Users table.
    Returns the user's Role (string) if valid, or None if invalid.
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
            return None  # username not found

        stored_hash = row[0]
        role = row[1]

        # bcrypt.checkpw compares the plain password against the stored hash
        if bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return role
        else:
            return None  # password incorrect

    finally:
        cursor.close()
        conn.close()