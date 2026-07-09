import tkinter as tk
from tkinter import messagebox, ttk
from datetime import date
from booking import (
    get_all_services, get_all_packages, get_service_price,
    get_available_staff, create_appointment
)


def open_booking_window(customer_id):
    win = tk.Toplevel()
    win.title("Book an Appointment")
    win.geometry("450x550")
    win.configure(bg='#F8F5F2')

    box = tk.Frame(win, width=400, height=500, bg="#FFFFFF",
                    highlightbackground="#D4AF37", highlightthickness=2)
    box.place(relx=0.5, rely=0.5, anchor='center')
    box.pack_propagate(False)

    tk.Label(box, text='Book Your Appointment', font=('Times new roman', 16, 'bold'),
              bg="#FFFFFF", fg="#3B3B3B").pack(pady=15)

    # Booking type: Service or Package
    booking_type = tk.StringVar(value="Service")
    type_frame = tk.Frame(box, bg="#FFFFFF")
    type_frame.pack(pady=5)
    tk.Radiobutton(type_frame, text="Service", variable=booking_type, value="Service",
                    bg="#FFFFFF", command=lambda: toggle_type()).pack(side="left", padx=10)
    tk.Radiobutton(type_frame, text="Package", variable=booking_type, value="Package",
                    bg="#FFFFFF", command=lambda: toggle_type()).pack(side="left", padx=10)

    # Service dropdown
    services = get_all_services()  # list of (ServiceID, Servicename)
    service_names = [s[1] for s in services]
    service_var = tk.StringVar()
    service_dropdown = ttk.Combobox(box, textvariable=service_var, values=service_names,
                                      width=30, state="readonly")

    # Staff type dropdown (only relevant for Services)
    staff_type_var = tk.StringVar(value="Junior")
    staff_dropdown = ttk.Combobox(box, textvariable=staff_type_var,
                                    values=["Senior", "Junior", "Intern"], width=30, state="readonly")

    # Package dropdown
    packages = get_all_packages()  # list of (PackageID, Packagename, Packageprice)
    package_names = [p[1] for p in packages]
    package_var = tk.StringVar()
    package_dropdown = ttk.Combobox(box, textvariable=package_var, values=package_names,
                                      width=30, state="readonly")

    tk.Label(box, text='Select Service:', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(15, 2))
    service_dropdown.pack()

    tk.Label(box, text='Staff Type:', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(10, 2))
    staff_dropdown.pack()

    price_label = tk.Label(box, text="Price: -", bg="#FFFFFF", font=("Arial", 13, "bold"), fg="#D4AF37")
    price_label.pack(pady=15)

    def toggle_type():
        if booking_type.get() == "Service":
            package_dropdown.pack_forget()
            service_dropdown.pack()
            staff_dropdown.pack()
        else:
            service_dropdown.pack_forget()
            staff_dropdown.pack_forget()
            package_dropdown.pack()
        price_label.config(text="Price: -")

    def update_price(*args):
        if booking_type.get() == "Service" and service_var.get() and staff_type_var.get():
            idx = service_names.index(service_var.get())
            service_id = services[idx][0]
            price = get_service_price(service_id, staff_type_var.get())
            price_label.config(text=f"Price: Rs. {price}" if price is not None else "Price: N/A")
        elif booking_type.get() == "Package" and package_var.get():
            idx = package_names.index(package_var.get())
            price = packages[idx][2]
            price_label.config(text=f"Price: Rs. {price}")

    service_var.trace_add("write", update_price)
    staff_type_var.trace_add("write", update_price)
    package_var.trace_add("write", update_price)

    def confirm_booking():
        today = date.today().isoformat()
        appt_time = "10:00:00"  # placeholder — could add a time picker later

        if booking_type.get() == "Service":
            if not service_var.get():
                messagebox.showerror("Error", "Please select a service.")
                return
            idx = service_names.index(service_var.get())
            service_id = services[idx][0]
            staff_type = staff_type_var.get()
            price = get_service_price(service_id, staff_type)

            if price is None:
                messagebox.showerror("Error", "No pricing found for this service/staff combination.")
                return

            staff_id = get_available_staff(staff_type)

            if staff_id is None:
                messagebox.showerror("Error", f"No {staff_type} staff available.")
                return

            success, result = create_appointment(
                customer_id, staff_id, service_id, None, today, appt_time, price
            )
        else:
            if not package_var.get():
                messagebox.showerror("Error", "Please select a package.")
                return
            idx = package_names.index(package_var.get())
            package_id = packages[idx][0]
            price = packages[idx][2]
            # For packages, still need SOME staff assigned — default to a Senior
            staff_id = get_available_staff("Senior")

            if staff_id is None:
                messagebox.showerror("Error", "No Senior staff available to handle this package.")
                return

            success, result = create_appointment(
                customer_id, staff_id, None, package_id, today, appt_time, price
            )

        if success:
            messagebox.showinfo("Booking Confirmed", f"Appointment #{result} booked! Price: Rs. {price}")
            win.destroy()
        else:
            messagebox.showerror("Error", result)

    tk.Button(box, text='Confirm Booking', bg="#D4AF37", fg="white", width=20,
              command=confirm_booking).pack(pady=20)