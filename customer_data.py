from db_connection import get_connection


def get_all_customers_full():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT CustomerID, FirstName, LastName, Email, Gender, LoyaltyPoints FROM Customer"
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_customers(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    like_term = f"%{keyword}%"
    cursor.execute(
        """SELECT CustomerID, FirstName, LastName, Email, Gender, LoyaltyPoints 
           FROM Customer 
           WHERE FirstName LIKE ? OR LastName LIKE ? OR Email LIKE ?""",
        (like_term, like_term, like_term)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_customer(first_name, last_name, email, gender):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ISNULL(MAX(CustomerID), 0) + 1 FROM Customer")
        new_id = cursor.fetchone()[0]
        cursor.execute(
            """INSERT INTO Customer (CustomerID, FirstName, LastName, Email, Gender, RegistrationDate)
               VALUES (?, ?, ?, ?, ?, CAST(GETDATE() AS DATE))""",
            (new_id, first_name, last_name, email, gender)
        )
        conn.commit()
        return True, new_id
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def update_customer(customer_id, first_name, last_name, email, gender):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Customer SET FirstName=?, LastName=?, Email=?, Gender=? 
               WHERE CustomerID=?""",
            (first_name, last_name, email, gender, customer_id)
        )
        conn.commit()
        return True, "Customer updated."
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Customer WHERE CustomerID=?", (customer_id,))
        conn.commit()
        return True, "Customer deleted."
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()