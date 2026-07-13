from db_connection import get_connection


def get_all_staff_full():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT StaffID, FirstName, LastName, Gender, StaffType, Specialization FROM Staff")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def search_staff(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    like_term = f"%{keyword}%"
    cursor.execute(
        """SELECT StaffID, FirstName, LastName, Gender, StaffType, Specialization 
           FROM Staff WHERE FirstName LIKE ? OR LastName LIKE ? OR Specialization LIKE ?""",
        (like_term, like_term, like_term)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_staff(first_name, last_name, gender, staff_type, specialization):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ISNULL(MAX(StaffID), 0) + 1 FROM Staff")
        new_id = cursor.fetchone()[0]
        cursor.execute(
            """INSERT INTO Staff (StaffID, FirstName, LastName, Gender, StaffType, Specialization)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (new_id, first_name, last_name, gender, staff_type, specialization)
        )
        conn.commit()
        return True, new_id
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def update_staff(staff_id, first_name, last_name, gender, staff_type, specialization):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Staff SET FirstName=?, LastName=?, Gender=?, StaffType=?, Specialization=? 
               WHERE StaffID=?""",
            (first_name, last_name, gender, staff_type, specialization, staff_id)
        )
        conn.commit()
        return True, "Staff updated."
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def delete_staff(staff_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Staff WHERE StaffID=?", (staff_id,))
        conn.commit()
        return True, "Staff deleted."
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()