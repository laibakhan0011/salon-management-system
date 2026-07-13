from db_connection import get_connection


def get_all_services_full():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ServiceID, Servicename, Baseprice, Duration FROM Service")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_service(name, price, duration):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ISNULL(MAX(ServiceID), 0) + 1 FROM Service")
        new_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO Service (ServiceID, Servicename, Baseprice, Duration) VALUES (?, ?, ?, ?)",
            (new_id, name, price, duration)
        )
        conn.commit()
        return True, new_id
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def update_service(service_id, name, price, duration):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Service SET Servicename=?, Baseprice=?, Duration=? WHERE ServiceID=?",
            (name, price, duration, service_id)
        )
        conn.commit()
        return True, "Service updated."
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def delete_service(service_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Service WHERE ServiceID=?", (service_id,))
        conn.commit()
        return True, "Service deleted."
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()