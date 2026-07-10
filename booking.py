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


def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT CustomerID, FirstName + ' ' + LastName FROM Customer")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return customers


def get_all_staff():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT StaffID, FirstName + ' ' + LastName, StaffType FROM Staff")
    staff = cursor.fetchall()
    cursor.close()
    conn.close()
    return staff


def book_appointment_via_procedure(customer_id, staff_id, service_id, appt_date, appt_time, price, payment_method):
    """Calls the BookAppointment stored procedure (handles appointment + payment as one transaction)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """EXEC BookAppointment 
               @CustomerID=?, @StaffID=?, @ServiceID=?, 
               @AppointmentDate=?, @AppointmentTime=?, @FinalPrice=?, @PaymentMethod=?""",
            (customer_id, staff_id, service_id, appt_date, appt_time, price, payment_method)
        )
        row = cursor.fetchone()
        conn.commit()
        if row and row[0] == 'Success':
            return True, row[1]  # AppointmentID
        else:
            return False, row[1] if row else "Unknown error"
    except Exception as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()


def get_pending_appointments():
    """Appointments that still need payment finalized."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT A.AppointmentID, C.FirstName + ' ' + C.LastName, A.FinalPrice
           FROM Appointment A
           JOIN Customer C ON A.CustomerID = C.CustomerID
           WHERE A.Status = 'Pending'"""
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def finalize_payment(appointment_id, final_total, payment_method):
    """Updates the Payment amount/method and marks the Appointment Completed, in one transaction."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE Payment SET Amount = ?, PaymentMethod = ? WHERE AppointmentID = ?",
            (final_total, payment_method, appointment_id)
        )
        cursor.execute(
            "UPDATE Appointment SET Status = 'Completed' WHERE AppointmentID = ?",
            (appointment_id,)
        )
        conn.commit()
        return True, "Payment finalized successfully."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()