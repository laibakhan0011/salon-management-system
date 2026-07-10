import tkinter as tk
from tkinter import messagebox, ttk
from booking import get_pending_appointments, finalize_payment


def open_payment_screen(root):
    win = tk.Toplevel(root)
    win.title("Process Payment")
    win.geometry("420x480")
    win.configure(bg='#F8F5F2')

    box = tk.Frame(win, width=370, height=430, bg="#FFFFFF",
                    highlightbackground="#D4AF37", highlightthickness=2)
    box.place(relx=0.5, rely=0.5, anchor='center')
    box.pack_propagate(False)

    tk.Label(box, text='Process Payment', font=('Times New Roman', 18, 'bold'),
              bg="#FFFFFF", fg="#3B3B3B").pack(pady=15)

    appointments = get_pending_appointments()
    appt_labels = [f"#{a[0]} - {a[1]} - Rs. {a[2]}" for a in appointments]
    appt_var = tk.StringVar()
    tk.Label(box, text='Appointment:', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(5, 2))
    appt_dropdown = ttk.Combobox(box, textvariable=appt_var, values=appt_labels, width=32, state="readonly")
    appt_dropdown.pack()

    method_var = tk.StringVar(value="Cash")
    tk.Label(box, text='Payment Method:', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(15, 2))
    method_dropdown = ttk.Combobox(box, textvariable=method_var,
                                     values=["Cash", "Card", "Online", "JazzCash"], width=32, state="readonly")
    method_dropdown.pack()

    tk.Label(box, text='Discount (Rs.):', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(15, 2))
    discount_entry = tk.Entry(box, width=32)
    discount_entry.insert(0, "0")
    discount_entry.pack()

    tk.Label(box, text='Tip (Rs.):', bg="#FFFFFF", font=("Arial", 10)).pack(pady=(10, 2))
    tip_entry = tk.Entry(box, width=32)
    tip_entry.insert(0, "0")
    tip_entry.pack()

    total_label = tk.Label(box, text="Final Total: Rs. -", bg="#FFFFFF", font=("Arial", 14, "bold"), fg="#D4AF37")
    total_label.pack(pady=15)

    def update_total(*args):
        if appt_var.get():
            idx = appt_labels.index(appt_var.get())
            base_price = appointments[idx][2]
            try:
                discount = float(discount_entry.get() or 0)
                tip = float(tip_entry.get() or 0)
                final = base_price - discount + tip
                total_label.config(text=f"Final Total: Rs. {final:.2f}")
            except ValueError:
                total_label.config(text="Final Total: invalid input")

    appt_var.trace_add("write", update_total)
    discount_entry.bind("<KeyRelease>", update_total)
    tip_entry.bind("<KeyRelease>", update_total)

    def save_payment():
        if not appt_var.get():
            messagebox.showerror("Error", "Please select an appointment.")
            return

        idx = appt_labels.index(appt_var.get())
        appointment_id = appointments[idx][0]
        base_price = appointments[idx][2]

        try:
            discount = float(discount_entry.get() or 0)
            tip = float(tip_entry.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Discount and Tip must be numbers.")
            return

        final_total = base_price - discount + tip

        success, message = finalize_payment(appointment_id, final_total, method_var.get())

        if success:
            messagebox.showinfo("Success", f"{message}\nFinal amount: Rs. {final_total:.2f}")
            win.destroy()
        else:
            messagebox.showerror("Error", message)

    tk.Button(box, text='Save Payment', bg="#D4AF37", fg="white", width=20,
              command=save_payment).pack(pady=10)