import tkinter as tk
from tkinter import ttk
from db_connection import get_connection
from datetime import date


def open_dashboard(root, role):
    dash_win = tk.Toplevel(root)
    dash_win.title('Salon Dashboard')
    dash_win.geometry('950x650')
    dash_win.protocol("WM_DELETE_WINDOW", root.destroy)
    dash_win.configure(bg='#F8F5F2')

    # ---- Title ----
    title = tk.Label(
        dash_win,
        text=f"Glow Salon Dashboard ({role})",
        font=('Times New Roman', 22, 'bold'),
        bg='#F8F5F2', fg='#3B3B3B'
    )
    title.pack(pady=15)

    # ---- Info boxes frame ----
    boxes_frame = tk.Frame(dash_win, bg='#F8F5F2')
    boxes_frame.pack(pady=10)

    def make_info_box(parent, label_text):
        box = tk.Frame(parent, bg="#FFFFFF", highlightbackground="#D4AF37",
                        highlightthickness=2, width=280, height=100)
        box.pack_propagate(False)
        tk.Label(box, text=label_text, bg="#FFFFFF", font=("Arial", 11), fg="#3B3B3B").pack(pady=(15, 5))
        value_label = tk.Label(box, text="0", bg="#FFFFFF", font=("Arial", 22, "bold"), fg="#D4AF37")
        value_label.pack()
        return box, value_label

    appt_box, appt_value = make_info_box(boxes_frame, "Today's Appointments")
    appt_box.grid(row=0, column=0, padx=10)

    revenue_box, revenue_value = make_info_box(boxes_frame, "Today's Revenue")
    revenue_box.grid(row=0, column=1, padx=10)

    customer_box, customer_value = make_info_box(boxes_frame, "Total Customers")
    customer_box.grid(row=0, column=2, padx=10)

    # ---- Treeview table ----
    table_frame = tk.Frame(dash_win, bg='#F8F5F2')
    table_frame.pack(pady=20, fill="both", expand=True, padx=20)

    columns = ("Date", "Customer", "Staff", "Service", "Status")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    tree.pack(fill="both", expand=True)

    # ---- Data loading functions ----
    def load_info_boxes():
        conn = get_connection()
        cursor = conn.cursor()
        today = date.today().isoformat()

        cursor.execute(
            "SELECT COUNT(*) FROM Appointment WHERE Appointmentdate = ?", (today,)
        )
        appt_value.config(text=str(cursor.fetchone()[0]))

        cursor.execute(
            "SELECT TotalRevenue FROM DailyRevenue WHERE PaymentDate = ?", (today,)
        )
        row = cursor.fetchone()
        revenue_value.config(text=f"Rs. {row[0]}" if row else "Rs. 0")

        cursor.execute("SELECT COUNT(*) FROM Customer")
        customer_value.config(text=str(cursor.fetchone()[0]))

        cursor.close()
        conn.close()

    def load_table():
        for row in tree.get_children():
            tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Appointmentdate, CustomerName, StaffName, ServiceName, Status FROM AppointmentDetails"
        )
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=tuple(row))

        cursor.close()
        conn.close()

    def refresh_all():
        load_info_boxes()
        load_table()

    # ---- Refresh button ----
    refresh_btn = tk.Button(
        dash_win, text="Refresh", bg="#D4AF37", fg="white",
        font=("Arial", 11), width=15, command=refresh_all
    )
    refresh_btn.pack(pady=10)

    # Load data immediately when dashboard opens
    refresh_all()