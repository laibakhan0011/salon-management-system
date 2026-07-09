import tkinter as tk
from tkinter import messagebox
from customer_auth import verify_customer_login
from customer_signup import open_customer_signup_window


def open_customer_login_window():
    login_win = tk.Toplevel()
    login_win.title("Glow Salon - Customer Login")
    login_win.geometry("400x400")
    login_win.configure(bg='#F8F5F2')

    login_box = tk.Frame(
        login_win,
        width=320,
        height=320,
        bg="#FFFFFF",
        highlightbackground="#D4AF37",
        highlightthickness=2
    )
    login_box.place(relx=0.5, rely=0.5, anchor='center')
    login_box.pack_propagate(False)

    tk.Label(login_box, text='Customer Login', font=('Times new roman', 18, 'bold'),
              bg="#FFFFFF", fg="#3B3B3B").pack(pady=20)

    tk.Label(login_box, text='Email', bg="#FFFFFF", font=("Arial", 11)).pack(anchor='w', padx=30)
    email_entry = tk.Entry(login_box, width=30, highlightthickness=2)
    email_entry.pack(pady=5)

    tk.Label(login_box, text='Password', bg="#FFFFFF", font=("Arial", 11)).pack(anchor='w', padx=30, pady=(10, 0))
    password_entry = tk.Entry(login_box, width=30, show='*', highlightthickness=2)
    password_entry.pack(pady=5)

    def handle_customer_login():
        email = email_entry.get().strip()
        password = password_entry.get()

        if not email or not password:
            messagebox.showerror("Login Failed", "Please enter both email and password.")
            return

        customer_id = verify_customer_login(email, password)

        if customer_id is None:
            messagebox.showerror("Login Failed", "Invalid email or password.")
        else:
            messagebox.showinfo("Success", "Login successful!")
            login_win.destroy()
            from booking_screen import open_booking_window
            open_booking_window(customer_id)

    tk.Button(login_box, text='Login', bg="#D4AF37", fg="white", width=20,
              command=handle_customer_login).pack(pady=20)

    signup_label = tk.Label(login_box, text="New customer? Sign Up", bg="#FFFFFF",
                              fg="#D4AF37", font=("Arial", 9, "underline"), cursor="hand2")
    signup_label.pack()
    signup_label.bind("<Button-1>", lambda e: open_customer_signup_window())