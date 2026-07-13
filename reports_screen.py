import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db_connection import get_connection
import csv


def open_reports_screen(root):
    win = tk.Toplevel(root)
    win.title("Reports")
    win.geometry("900x650")
    win.configure(bg='#F8F5F2')

    tk.Label(win, text="Salon Reports", font=('Times New Roman', 20, 'bold'),
              bg='#F8F5F2', fg='#3B3B3B').pack(pady=10)

    # ---- Staff Ranked by Revenue ----
    tk.Label(win, text="Staff Ranked by Revenue", font=('Arial', 13, 'bold'),
              bg='#F8F5F2', fg='#D4AF37').pack(pady=(10, 5))

    staff_columns = ("Rank", "Staff Name", "Total Revenue")
    staff_tree = ttk.Treeview(win, columns=staff_columns, show="headings", height=8)
    for col in staff_columns:
        staff_tree.heading(col, text=col)
        staff_tree.column(col, width=200, anchor="center")
    staff_tree.pack(pady=5, padx=20, fill="x")

    # ---- Top Services ----
    tk.Label(win, text="Top Services (by bookings)", font=('Arial', 13, 'bold'),
              bg='#F8F5F2', fg='#D4AF37').pack(pady=(20, 5))

    service_columns = ("Service Name", "Total Bookings", "Total Revenue")
    service_tree = ttk.Treeview(win, columns=service_columns, show="headings", height=8)
    for col in service_columns:
        service_tree.heading(col, text=col)
        service_tree.column(col, width=200, anchor="center")
    service_tree.pack(pady=5, padx=20, fill="x")

    staff_data_cache = []
    service_data_cache = []

    def load_reports():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 
                    S.FirstName + ' ' + S.LastName AS StaffName,
                    ISNULL(SUM(P.Amount), 0) AS TotalRevenue,
                    RANK() OVER (ORDER BY ISNULL(SUM(P.Amount), 0) DESC) AS RevenueRank
                FROM Staff S
                LEFT JOIN Appointment A ON S.StaffID = A.StaffID
                LEFT JOIN Payment P ON A.AppointmentID = P.AppointmentID
                GROUP BY S.StaffID, S.FirstName, S.LastName
                ORDER BY RevenueRank
            """)
            staff_rows = cursor.fetchall()

            cursor.execute("""
                SELECT 
                    SV.Servicename,
                    COUNT(A.AppointmentID) AS TotalBookings,
                    ISNULL(SUM(P.Amount), 0) AS TotalRevenue
                FROM Service SV
                LEFT JOIN Appointment A ON SV.ServiceID = A.ServiceID
                LEFT JOIN Payment P ON A.AppointmentID = P.AppointmentID
                GROUP BY SV.ServiceID, SV.Servicename
                ORDER BY TotalBookings DESC
            """)
            service_rows = cursor.fetchall()

            cursor.close()
            conn.close()

            for row in staff_tree.get_children():
                staff_tree.delete(row)
            staff_data_cache.clear()
            for row in staff_rows:
                display_row = (row[2], row[0], f"Rs. {row[1]}")
                staff_tree.insert("", "end", values=display_row)
                staff_data_cache.append(display_row)

            for row in service_tree.get_children():
                service_tree.delete(row)
            service_data_cache.clear()
            for row in service_rows:
                display_row = (row[0], row[1], f"Rs. {row[2]}")
                service_tree.insert("", "end", values=display_row)
                service_data_cache.append(display_row)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def export_to_csv():
        try:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save Report As"
            )
            if not filepath:
                return

            with open(filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["-- Staff Ranked by Revenue --"])
                writer.writerow(["Rank", "Staff Name", "Total Revenue"])
                writer.writerows(staff_data_cache)
                writer.writerow([])
                writer.writerow(["-- Top Services --"])
                writer.writerow(["Service Name", "Total Bookings", "Total Revenue"])
                writer.writerows(service_data_cache)

            messagebox.showinfo("Success", f"Report exported to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    btn_frame = tk.Frame(win, bg='#F8F5F2')
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Refresh Reports", bg="#D4AF37", fg="white", width=18, command=load_reports).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Export to CSV", bg="#3B3B3B", fg="white", width=18, command=export_to_csv).pack(side="left", padx=10)

    load_reports()