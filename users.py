import bcrypt
from db_connection import get_connection

def hash_password(plain_password):
    """
    Converts a plain text password into a secure bcrypt hash.
    bcrypt automatically generates a random 'salt' each time,
    so even identical passwords produce different hashes.
    """
    password_bytes = plain_password.encode('utf-8')  # bcrypt needs bytes, not string
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')  # store as a normal string in the database


def create_user(username, plain_password, role):
    conn = get_connection()
    if conn is None:
        print("Could not connect to database.")
        return

    cursor = conn.cursor()
    hashed_pw = hash_password(plain_password)

    try:
        cursor.execute(
            "INSERT INTO Users (Username, Password, Role) VALUES (?, ?, ?)",
            (username, hashed_pw, role)
        )
        conn.commit()
        print(f"User '{username}' created successfully as {role}.")
    except Exception as e:
        print("Error creating user:", e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # Create one Admin and one Receptionist test user
    create_user("admin1", "Admin@123", "Admin")
    create_user("reception1", "Reception@123", "Receptionist")



