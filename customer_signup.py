import tkinter as tk
from tkinter import messagebox
from customer_auth import create_customer_account


def open_customer_signup_window():
    signup_win = tk.Toplevel()
    signup_win.title("Glow Salon - Customer Sign Up")
    signup_win.geometry("400x520")
    signup_win.configure(bg='#F8F5F2')

    signup_box = tk.Frame(
        signup_win, width=340, height=470, bg="#FFFFFF",
        highlightbackground="#D4AF37", highlightthickness=2
    )
    signup_box.place(relx=0.5, rely=0.5, anchor='center')
    signup_box.pack_propagate(False)

    tk.Label(signup_box, text='Create Account', font=('Times new roman', 18, 'bold'),
              bg="#FFFFFF", fg="#3B3B3B").pack(pady=15)

    tk.Label(signup_box, text='First Name', bg="#FFFFFF", font=("Arial", 10)).pack(anchor='w', padx=35)
    fname_entry = tk.Entry(signup_box, width=30)
    fname_entry.pack(pady=4)

    tk.Label(signup_box, text='Last Name', bg="#FFFFFF", font=("Arial", 10)).pack(anchor='w', padx=35, pady=(8, 0))
    lname_entry = tk.Entry(signup_box, width=30)
    lname_entry.pack(pady=4)

    tk.Label(signup_box, text='Email', bg="#FFFFFF", font=("Arial", 10)).pack(anchor='w', padx=35, pady=(8, 0))
    email_entry = tk.Entry(signup_box, width=30)
    email_entry.pack(pady=4)

    tk.Label(signup_box, text='Password', bg="#FFFFFF", font=("Arial", 10)).pack(anchor='w', padx=35, pady=(8, 0))
    password_entry = tk.Entry(signup_box, width=30, show='*')
    password_entry.pack(pady=4)

    tk.Label(signup_box, text='Gender (M/F)', bg="#FFFFFF", font=("Arial", 10)).pack(anchor='w', padx=35, pady=(8, 0))
    gender_entry = tk.Entry(signup_box, width=30)
    gender_entry.pack(pady=4)

    def handle_signup():
        fname = fname_entry.get().strip()
        lname = lname_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()
        gender = gender_entry.get().strip().upper()

        if not all([fname, lname, email, password, gender]):
            messagebox.showerror("Signup Failed", "Please fill in all fields.")
            return

        if gender not in ('M', 'F'):
            messagebox.showerror("Signup Failed", "Gender must be M or F.")
            return

        if len(password) < 6:
            messagebox.showerror("Signup Failed", "Password must be at least 6 characters.")
            return

        success, result = create_customer_account(fname, lname, email, password, gender)

        if success:
            messagebox.showinfo("Success", f"Account created! Your Customer ID is {result}.")
            signup_win.destroy()
        else:
            messagebox.showerror("Signup Failed", result)

    tk.Button(signup_box, text='Sign Up', bg="#D4AF37", fg="white", width=20,
              command=handle_signup).pack(pady=20)