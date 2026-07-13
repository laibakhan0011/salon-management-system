import tkinter as tk
from tkinter import messagebox, ttk
from staff_data import get_all_staff_full, search_staff, add_staff, update_staff, delete_staff


def open_staff_screen(root):
    win = tk.Toplevel(root)
    win.title("Manage Staff")
    win.geometry("900x600")
    win.configure(bg='#F8F5F2')

    tk.Label(win, text="Manage Staff", font=('Times New Roman', 20, 'bold'),
              bg='#F8F5F2', fg='#3B3B3B').pack(pady=10)

    search_frame = tk.Frame(win, bg='#F8F5F2')
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Search:", bg='#F8F5F2').pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, width=30)
    search_entry.pack(side="left", padx=5)

    form_frame = tk.Frame(win, bg='#F8F5F2')
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="First Name", bg='#F8F5F2').grid(row=0, column=0, padx=5)
    fname_entry = tk.Entry(form_frame, width=13)
    fname_entry.grid(row=1, column=0, padx=5)

    tk.Label(form_frame, text="Last Name", bg='#F8F5F2').grid(row=0, column=1, padx=5)
    lname_entry = tk.Entry(form_frame, width=13)
    lname_entry.grid(row=1, column=1, padx=5)

    tk.Label(form_frame, text="Gender", bg='#F8F5F2').grid(row=0, column=2, padx=5)
    gender_entry = tk.Entry(form_frame, width=6)
    gender_entry.grid(row=1, column=2, padx=5)

    tk.Label(form_frame, text="Staff Type", bg='#F8F5F2').grid(row=0, column=3, padx=5)
    type_var = tk.StringVar(value="Junior")
    type_dropdown = ttk.Combobox(form_frame, textvariable=type_var, values=["Senior", "Junior", "Intern"], width=10, state="readonly")
    type_dropdown.grid(row=1, column=3, padx=5)

    tk.Label(form_frame, text="Specialization", bg='#F8F5F2').grid(row=0, column=4, padx=5)
    spec_entry = tk.Entry(form_frame, width=15)
    spec_entry.grid(row=1, column=4, padx=5)

    selected_id = tk.IntVar(value=0)

    columns = ("ID", "First Name", "Last Name", "Gender", "Type", "Specialization")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(pady=10, fill="both", expand=True, padx=20)

    def refresh_table(rows=None):
        for row in tree.get_children():
            tree.delete(row)
        data = rows if rows is not None else get_all_staff_full()
        for row in data:
            tree.insert("", "end", values=tuple(row))

    def on_row_select(event):
        selected = tree.selection()
        if not selected:
            return
        values = tree.item(selected[0])['values']
        selected_id.set(values[0])
        fname_entry.delete(0, tk.END); fname_entry.insert(0, values[1])
        lname_entry.delete(0, tk.END); lname_entry.insert(0, values[2])
        gender_entry.delete(0, tk.END); gender_entry.insert(0, values[3])
        type_var.set(values[4])
        spec_entry.delete(0, tk.END); spec_entry.insert(0, values[5])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    def clear_form():
        selected_id.set(0)
        fname_entry.delete(0, tk.END)
        lname_entry.delete(0, tk.END)
        gender_entry.delete(0, tk.END)
        type_var.set("Junior")
        spec_entry.delete(0, tk.END)

    def do_search():
        keyword = search_entry.get().strip()
        refresh_table(search_staff(keyword) if keyword else None)

    def do_add():
        try:
            if not all([fname_entry.get(), lname_entry.get(), gender_entry.get(), spec_entry.get()]):
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            success, result = add_staff(fname_entry.get(), lname_entry.get(),
                                          gender_entry.get().upper(), type_var.get(), spec_entry.get())
            if success:
                messagebox.showinfo("Success", f"Staff added (ID {result}).")
                clear_form(); refresh_table()
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def do_update():
        try:
            if selected_id.get() == 0:
                messagebox.showerror("Error", "Select a staff member first.")
                return
            success, result = update_staff(selected_id.get(), fname_entry.get(), lname_entry.get(),
                                             gender_entry.get().upper(), type_var.get(), spec_entry.get())
            if success:
                messagebox.showinfo("Success", result)
                clear_form(); refresh_table()
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def do_delete():
        try:
            if selected_id.get() == 0:
                messagebox.showerror("Error", "Select a staff member first.")
                return
            if not messagebox.askyesno("Confirm", "Delete this staff member?"):
                return
            success, result = delete_staff(selected_id.get())
            if success:
                messagebox.showinfo("Success", result)
                clear_form(); refresh_table()
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