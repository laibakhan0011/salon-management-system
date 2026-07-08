import pyodbc

def get_connection():
    """
    Creates and returns a connection to the SQL Server database.
    Uses Windows Authentication (Trusted_Connection), so no username/password needed.
    """
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=Salon_managment_system;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print("Database connection failed:", e)
        return None


# Quick test — only runs when you execute this file directly
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Connected successfully!")
        conn.close()
    else:
        print("Connection failed.")