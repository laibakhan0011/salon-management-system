import bcrypt
from db_connection import get_connection


def hash_password(plain_password):
    password_bytes = plain_password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_customer_login(email, plain_password):
    """
    Checks email + password against the Customer table.
    Returns CustomerID if valid, or None if invalid.
    """
    conn = get_connection()
    if conn is None:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT CustomerID, Password FROM Customer WHERE Email = ?",
            (email,)
        )
        row = cursor.fetchone()

        if row is None or row[1] is None:
            return None  # no account or never signed up with a password

        customer_id = row[0]
        stored_hash = row[1]

        if bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return customer_id
        else:
            return None

    finally:
        cursor.close()
        conn.close()


def create_customer_account(first_name, last_name, email, plain_password, gender):
    """
    Creates a new Customer account (self-signup).
    Returns (True, CustomerID) or (False, "error message").
    """
    conn = get_connection()
    if conn is None:
        return False, "Could not connect to database."

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT CustomerID FROM Customer WHERE Email = ?", (email,))
        if cursor.fetchone() is not None:
            return False, "An account with this email already exists."

        hashed_pw = hash_password(plain_password)

        # Get the next available CustomerID (since your table uses manual INT PKs, not IDENTITY)
        cursor.execute("SELECT ISNULL(MAX(CustomerID), 0) + 1 FROM Customer")
        new_id = cursor.fetchone()[0]

        cursor.execute(
            """INSERT INTO Customer (CustomerID, FirstName, LastName, Email, Password, Gender, RegistrationDate)
               VALUES (?, ?, ?, ?, ?, ?, CAST(GETDATE() AS DATE))""",
            (new_id, first_name, last_name, email, hashed_pw, gender)
        )
        conn.commit()
        return True, new_id

    except Exception as e:
        return False, f"Error creating account: {e}"

    finally:
        cursor.close()
        conn.close()








