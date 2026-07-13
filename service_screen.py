import tkinter as tk
from tkinter import messagebox, ttk
from service_data import get_all_services_full, add_service, update_service, delete_service


def open_service_screen(root):
    win = tk.Toplevel(root)
    win.title("Manage Services")
    win.geometry("700x550")
    win.configure(bg='#F8F5F2')

    tk.Label(win, text="Manage Services", font=('Times New Roman', 20, 'bold'),
              bg='#F8F5F2', fg='#3B3B3B').pack(pady=10)

    form_frame = tk.Frame(win, bg='#F8F5F2')
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Service Name", bg='#F8F5F2').grid(row=0, column=0, padx=5)
    name_entry = tk.Entry(form_frame, width=20)
    name_entry.grid(row=1, column=0, padx=5)

    tk.Label(form_frame, text="Base Price", bg='#F8F5F2').grid(row=0, column=1, padx=5)
    price_entry = tk.Entry(form_frame, width=10)
    price_entry.grid(row=1, column=1, padx=5)

    tk.Label(form_frame, text="Duration (min)", bg='#F8F5F2').grid(row=0, column=2, padx=5)
    duration_entry = tk.Entry(form_frame, width=10)
    duration_entry.grid(row=1, column=2, padx=5)

    selected_id = tk.IntVar(value=0)

    columns = ("ID", "Name", "Base Price", "Duration")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")
    tree.pack(pady=10, fill="both", expand=True, padx=20)

    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        for row in get_all_services_full():
            tree.insert("", "end", values=tuple(row))

    def on_row_select(event):
        selected = tree.selection()
        if not selected:
            return
        values = tree.item(selected[0])['values']
        selected_id.set(values[0])
        name_entry.delete(0, tk.END); name_entry.insert(0, values[1])
        price_entry.delete(0, tk.END); price_entry.insert(0, values[2])
        duration_entry.delete(0, tk.END); duration_entry.insert(0, values[3])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    def clear_form():
        selected_id.set(0)
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        duration_entry.delete(0, tk.END)

    def do_add():
        try:
            if not all([name_entry.get(), price_entry.get(), duration_entry.get()]):
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            success, result = add_service(name_entry.get(), int(price_entry.get()), int(duration_entry.get()))
            if success:
                messagebox.showinfo("Success", f"Service added (ID {result}).")
                clear_form(); refresh_table()
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showerror("Error", "Price and Duration must be numbers.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def do_update():
        try:
            if selected_id.get() == 0:
                messagebox.showerror("Error", "Select a service first.")
                return
            success, result = update_service(selected_id.get(), name_entry.get(),
                                               int(price_entry.get()), int(duration_entry.get()))
            if success:
                messagebox.showinfo("Success", result)
                clear_form(); refresh_table()
            else:
                messagebox.showerror("Error", result)
        except ValueError:
            messagebox.showerror("Error", "Price and Duration must be numbers.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def do_delete():
        try:
            if selected_id.get() == 0:
                messagebox.showerror("Error", "Select a service first.")
                return
            if not messagebox.askyesno("Confirm", "Delete this service?"):
                return
            success, result = delete_service(selected_id.get())
            if success:
                messagebox.showinfo("Success", result)
                clear_form(); refresh_table()
            else:
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    btn_frame = tk.Frame(win, bg='#F8F5F2')
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add", bg="#D4AF37", fg="white", width=12, command=do_add).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Update", bg="#3B3B3B", fg="white", width=12, command=do_update).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete", bg="#B22222", fg="white", width=12, command=do_delete).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear Form", bg="#888888", fg="white", width=12, command=clear_form).pack(side="left", padx=5)

    refresh_table()