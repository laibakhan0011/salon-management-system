import tkinter as tk
from tkinter import messagebox, ttk
from customer_data import get_all_customers_full, search_customers, add_customer, update_customer, delete_customer


def open_customer_screen(root):
    win = tk.Toplevel(root)
    win.title("Manage Customers")
    win.geometry("900x600")
    win.configure(bg='#F8F5F2')

    tk.Label(win, text="Manage Customers", font=('Times New Roman', 20, 'bold'),
              bg='#F8F5F2', fg='#3B3B3B').pack(pady=10)

    # ---- Search bar ----
    search_frame = tk.Frame(win, bg='#F8F5F2')
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Search:", bg='#F8F5F2').pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side="left", padx=5)

    # ---- Form fields ----
    form_frame = tk.Frame(win, bg='#F8F5F2')
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="First Name", bg='#F8F5F2').grid(row=0, column=0, padx=5)
    fname_entry = tk.Entry(form_frame, width=15)
    fname_entry.grid(row=1, column=0, padx=5)

    tk.Label(form_frame, text="Last Name", bg='#F8F5F2').grid(row=0, column=1, padx=5)
    lname_entry = tk.Entry(form_frame, width=15)
    lname_entry.grid(row=1, column=1, padx=5)

    tk.Label(form_frame, text="Email", bg='#F8F5F2').grid(row=0, column=2, padx=5)
    email_entry = tk.Entry(form_frame, width=20)
    email_entry.grid(row=1, column=2, padx=5)

    tk.Label(form_frame, text="Gender (M/F)", bg='#F8F5F2').grid(row=0, column=3, padx=5)
    gender_entry = tk.Entry(form_frame, width=8)
    gender_entry.grid(row=1, column=3, padx=5)

    selected_id = tk.IntVar(value=0)  # tracks which row is currently selected for update/delete

    # ---- Table ----
    columns = ("ID", "First Name", "Last Name", "Email", "Gender", "Loyalty Points")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(pady=10, fill="both", expand=True, padx=20)

    def refresh_table(rows=None):
        for row in tree.get_children():
            tree.delete(row)
        data = rows if rows is not None else get_all_customers_full()
        for row in data:
            tree.insert("", "end", values=tuple(row))

    def on_row_select(event):
        selected = tree.selection()
        if not selected:
            return
        values = tree.item(selected[0])['values']
        selected_id.set(values[0])
        fname_entry.delete(0, tk.END)
        fname_entry.insert(0, values[1])
        lname_entry.delete(0, tk.END)
        lname_entry.insert(0, values[2])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[3])
        gender_entry.delete(0, tk.END)
        gender_entry.insert(0, values[4])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    def clear_form():
        selected_id.set(0)
        fname_entry.delete(0, tk.END)
        lname_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        gender_entry.delete(0, tk.END)

    def do_search():
        keyword = search_entry.get().strip()
        if keyword:
            refresh_table(search_customers(keyword))
        else:
            refresh_table()

    def do_add():
        try:
            fname, lname, email, gender = fname_entry.get(), lname_entry.get(), email_entry.get(), gender_entry.get().upper()
            if not all([fname, lname, email, gender]):
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            success, result = add_customer(fname, lname, email, gender)
            if success:
                messagebox.showinfo("Success", f"Customer added (ID {result}).")
                clear_form()
                refresh_table()
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def do_update():
        try:
            if selected_id.get() == 0:
                messagebox.showerror("Error", "Please select a customer from the table first.")
                return
            fname, lname, email, gender = fname_entry.get(), lname_entry.get(), email_entry.get(), gender_entry.get().upper()
            success, result = update_customer(selected_id.get(), fname, lname, email, gender)
            if success:
                messagebox.showinfo("Success", result)
                clear_form()
                refresh_table()
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def do_delete():
        try:
            if selected_id.get() == 0:
                messagebox.showerror("Error", "Please select a customer from the table first.")
                return
            if not messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
                return
            success, result = delete_customer(selected_id.get())
            if success:
                messagebox.showinfo("Success", result)
                clear_form()
                refresh_table()
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(search_frame, text="Search", bg="#D4AF37", fg="white", command=do_search).pack(side="left", padx=5)
    tk.Button(search_frame, text="Clear", bg="#3B3B3B", fg="white", command=lambda: [search_entry.delete(0, tk.END), refresh_table()]).pack(side="left", padx=5)

    btn_frame = tk.Frame(win, bg='#F8F5F2')
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Add", bg="#D4AF37", fg="white", width=12, command=do_add).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Update", bg="#3B3B3B", fg="white", width=12, command=do_update).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete", bg="#B22222", fg="white", width=12, command=do_delete).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear Form", bg="#888888", fg="white", width=12, command=clear_form).pack(side="left", padx=5)

    refresh_table()