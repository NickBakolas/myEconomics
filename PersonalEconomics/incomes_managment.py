import tkinter as tk
from tkinter import ttk, messagebox

income_window_ref = None  # Χρησιμοποιείται για να ανοίγει μόνο μία φορά

def open_income_details_window(main_app):
    global income_window_ref

    if income_window_ref is not None and income_window_ref.winfo_exists():
        income_window_ref.lift()
        income_window_ref.focus_force()
        return

    income_window_ref = tk.Toplevel()
    window = income_window_ref
    window.title("Λίστα Εσόδων")
    window.geometry("800x400")

    def on_close():
        global income_window_ref
        income_window_ref = None
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    category_map = {cat_id: name for cat_id, name in main_app.categories}

    tree = ttk.Treeview(window, columns=("id", "name", "value", "category", "monthly", "date"), show="headings")
    for col, text in zip(tree["columns"], ["ID", "Περιγραφή", "Ποσό", "Κατηγορία", "Μηνιαίο", "Ημερομηνία"]):
        tree.heading(col, text=text)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_data():
        tree.delete(*tree.get_children())
        try:
            data = main_app.get_income()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία φόρτωσης εσόδων: {e}")
            return
        for row in data:
            id_, name, value, cat_id, monthly, date = row
            category = category_map.get(cat_id, "Άγνωστη")
            monthly_text = "Ναι" if monthly else "Όχι"
            tree.insert("", "end", values=(id_, name, value, category, monthly_text, date))

    def delete_income():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return
        income_id = tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Επιβεβαίωση", f"Διαγραφή εισοδήματος με ID {income_id};"):
            try:
                main_app.delete_income(income_id)
                load_data()
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Σφάλμα διαγραφής: {e}")

    def edit_income():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return
        values = tree.item(selected[0])["values"]
        income_id, name, value, category, monthly, date = values

        edit_win = tk.Toplevel(window)
        edit_win.title("Επεξεργασία Εισοδήματος")
        edit_win.geometry("350x300")

        tk.Label(edit_win, text="Περιγραφή").pack()
        name_entry = tk.Entry(edit_win)
        name_entry.insert(0, name)
        name_entry.pack()

        tk.Label(edit_win, text="Ποσό").pack()
        value_entry = tk.Entry(edit_win)
        value_entry.insert(0, str(value))
        value_entry.pack()

        tk.Label(edit_win, text="Ημερομηνία").pack()
        date_entry = tk.Entry(edit_win)
        date_entry.insert(0, date)
        date_entry.pack()

        monthly_var = tk.BooleanVar(value=(monthly == "Ναι"))
        tk.Checkbutton(edit_win, text="Μηνιαίο", variable=monthly_var).pack(pady=5)

        def save_changes():
            try:
                main_app.edit_income(
                    income_id,
                    name=name_entry.get(),
                    value=float(value_entry.get()),
                    date=date_entry.get(),
                    monthly=monthly_var.get()
                )
                edit_win.destroy()
                load_data()
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Αποτυχία αποθήκευσης αλλαγών: {e}")

        tk.Button(edit_win, text="Αποθήκευση", command=save_changes).pack(pady=10)

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Επεξεργασία", command=edit_income).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Διαγραφή", command=delete_income).pack(side="left", padx=10)

    load_data()
