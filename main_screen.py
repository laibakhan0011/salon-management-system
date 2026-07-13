import tkinter as tk
from customer_screen import open_customer_screen
from staff_screen import open_staff_screen
from service_screen import open_service_screen
from reports_screen import open_reports_screen
from dashboard_screen import open_dashboard
from new_appointment_screen import open_new_appointment_screen
from payment_screen import open_payment_screen


def open_main_menu(login_root, role):
    menu_win = tk.Toplevel(login_root)
    menu_win.title("Glow Salon - Main Menu")
    menu_win.geometry("900x600")
    menu_win.configure(bg='#F8F5F2')
    menu_win.protocol("WM_DELETE_WINDOW", login_root.destroy)

    # ---- Side menu ----
    side_menu = tk.Frame(menu_win, bg='#3B3B3B', width=200)
    side_menu.pack(side="left", fill="y")
    side_menu.pack_propagate(False)

    tk.Label(side_menu, text="Glow Salon", font=('Times New Roman', 16, 'bold'),
              bg='#3B3B3B', fg='#D4AF37').pack(pady=20)

    tk.Label(side_menu, text=f"Logged in as {role}", bg='#3B3B3B', fg='white',
              font=('Arial', 9)).pack(pady=(0, 20))

    def make_menu_button(text, command):
        tk.Button(side_menu, text=text, bg='#3B3B3B', fg='white', bd=0,
                   font=('Arial', 11), width=20, anchor="w", padx=15,
                   activebackground='#D4AF37', command=command).pack(pady=2, fill="x")

    make_menu_button("Dashboard", lambda: open_dashboard(menu_win, role))
    make_menu_button("Customers", lambda: open_customer_screen(menu_win))
    make_menu_button("Staff", lambda: open_staff_screen(menu_win))
    make_menu_button("Services", lambda: open_service_screen(menu_win))
    make_menu_button("New Appointment", lambda: open_new_appointment_screen(menu_win))
    make_menu_button("Process Payment", lambda: open_payment_screen(menu_win))
    make_menu_button("Reports", lambda: open_reports_screen(menu_win))

    def logout():
        menu_win.destroy()
        login_root.deiconify()

    tk.Button(side_menu, text="Logout", bg='#B22222', fg='white', bd=0,
               font=('Arial', 11, 'bold'), width=20, command=logout).pack(side="bottom", pady=20, fill="x")

    # ---- Main content area (welcome placeholder) ----
    content_area = tk.Frame(menu_win, bg='#F8F5F2')
    content_area.pack(side="right", fill="both", expand=True)

    tk.Label(content_area, text=f"Welcome, {role}!", font=('Times New Roman', 24, 'bold'),
              bg='#F8F5F2', fg='#3B3B3B').pack(expand=True)