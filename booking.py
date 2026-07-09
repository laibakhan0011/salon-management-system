from db_connection import get_connection


def get_all_services():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ServiceID, Servicename FROM Service")
    services = cursor.fetchall()
    cursor.close()
    conn.close()
    return services


def get_all_packages():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT PackageID, Packagename, Packageprice FROM Package")
    packages = cursor.fetchall()
    cursor.close()
    conn.close()
    return packages


def get_service_price(service_id, staff_type):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT Price FROM ServicePricing WHERE ServiceID = ? AND StaffType = ?",
        (service_id, staff_type)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None


def get_available_staff(staff_type):
    """Returns the first StaffID matching the chosen type."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT TOP 1 StaffID FROM Staff WHERE StaffType = ?",
        (staff_type,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None


def create_appointment(customer_id, staff_id, service_id, package_id, appt_date, appt_time, final_price):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ISNULL(MAX(AppointmentID), 0) + 1 FROM Appointment")
        new_id = cursor.fetchone()[0]

        cursor.execute(
            """INSERT INTO Appointment 
               (AppointmentID, CustomerID, StaffID, ServiceID, PackageID, Appointmentdate, Appointmenttime, Status, FinalPrice)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending', ?)""",
            (new_id, customer_id, staff_id, service_id, package_id, appt_date, appt_time, final_price)
        )
        conn.commit()
        return True, new_id
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()