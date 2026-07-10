import tkinter as tk
from tkinter import messagebox, ttk
from booking import get_all_customers, get_all_staff, get_all_services, get_service_price, book_appointment_via_procedure


def open_new_appointment_screen(root):
    win = tk.Toplevel(root)
    win.title("New Appointment")
    win.geometry("450x600")
    win.configure(bg='#F8F5F2')

    box = tk.Frame(win, width=400, height=550, bg="#FFFFFF",
                    highlightbackground="#D4AF37", highlightthickness=2)
    box.place(relx=0.5, rely=0.5, anchor='center')
    box.pack_propagate(False)

    tk.Label(box, text='New Appointment', font=('Times New Roman', 18, 'bold'),
              bg="#FFFFFF", fg="#3B3B3B").pack(pady=15)

    customers = get_all_customers()
    customer_names = [c[1] for c in customers]
    customer_var = tk.StringVar()
    tk.Label(box, text='Customer:', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(5, 2))
    customer_dropdown = ttk.Combobox(box, textvariable=customer_var, values=customer_names, width=30, state="readonly")
    customer_dropdown.pack()

    staff = get_all_staff()
    staff_names = [f"{s[1]} ({s[2]})" for s in staff]
    staff_var = tk.StringVar()
    tk.Label(box, text='Staff:', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(10, 2))
    staff_dropdown = ttk.Combobox(box, textvariable=staff_var, values=staff_names, width=30, state="readonly")
    staff_dropdown.pack()

    services = get_all_services()
    service_names = [s[1] for s in services]
    service_var = tk.StringVar()
    tk.Label(box, text='Service:', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(10, 2))
    service_dropdown = ttk.Combobox(box, textvariable=service_var, values=service_names, width=30, state="readonly")
    service_dropdown.pack()

    tk.Label(box, text='Date (YYYY-MM-DD):', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(10, 2))
    date_entry = tk.Entry(box, width=30)
    date_entry.pack()

    tk.Label(box, text='Time (HH:MM:SS):', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(10, 2))
    time_entry = tk.Entry(box, width=30)
    time_entry.pack()

    price_label = tk.Label(box, text="Price: -", bg="#FFFFFF", font=("Arial", 14, "bold"), fg="#D4AF37")
    price_label.pack(pady=15)

    def update_price(*args):
        if staff_var.get() and service_var.get():
            staff_idx = staff_names.index(staff_var.get())
            staff_type = staff[staff_idx][2]
            service_idx = service_names.index(service_var.get())
            service_id = services[service_idx][0]
            price = get_service_price(service_id, staff_type)
            price_label.config(text=f"Price: Rs. {price}" if price else "Price: N/A")

    staff_var.trace_add("write", update_price)
    service_var.trace_add("write", update_price)

    def clear_form():
        customer_var.set('')
        staff_var.set('')
        service_var.set('')
        date_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        price_label.config(text="Price: -")

    def book_now():
        if not all([customer_var.get(), staff_var.get(), service_var.get(),
                    date_entry.get(), time_entry.get()]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        customer_id = customers[customer_names.index(customer_var.get())][0]
        staff_idx = staff_names.index(staff_var.get())
        staff_id = staff[staff_idx][0]
        staff_type = staff[staff_idx][2]
        service_id = services[service_names.index(service_var.get())][0]
        price = get_service_price(service_id, staff_type)

        if price is None:
            messagebox.showerror("Error", "No price found for this combination.")
            return

        success, result = book_appointment_via_procedure(
            customer_id, staff_id, service_id,
            date_entry.get(), time_entry.get(), price, "Cash"
        )

        if success:
            messagebox.showinfo("Success", f"Appointment #{result} booked! Price: Rs. {price}")
            clear_form()
        else:
            messagebox.showerror("Booking Failed", result)

    tk.Button(box, text='Book Now', bg="#D4AF37", fg="white", width=20,
              command=book_now).pack(pady=20)