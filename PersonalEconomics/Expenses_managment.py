import tkinter as tk
from tkinter import ttk, messagebox

expense_window_ref = None  # ✅ Μόνο εδώ!

def open_expenses_details_window(main_app):
    global expense_window_ref

    if expense_window_ref is not None and expense_window_ref.winfo_exists():
        expense_window_ref.lift()
        expense_window_ref.focus_force()
        return

    expense_window_ref = tk.Toplevel()
    window = expense_window_ref
    window.title("Λίστα Εξόδων")
    window.geometry("800x400")

    def on_close():
        global expense_window_ref
        expense_window_ref = None
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
            data = main_app.get_expense()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία φόρτωσης εξόδων: {e}")
            return
        for row in data:
            id_, name, value, cat_id, monthly, date = row
            category = category_map.get(cat_id, "Άγνωστη")
            monthly_text = "Ναι" if monthly else "Όχι"
            tree.insert("", "end", values=(id_, name, value, category, monthly_text, date))

    def delete_expense():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return
        expense_id = tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Επιβεβαίωση", f"Διαγραφή εξόδου με ID {expense_id};"):
            try:
                main_app.delete_expense(expense_id)
                load_data()
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Σφάλμα διαγραφής: {e}")

    def edit_expense():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return
        values = tree.item(selected[0])["values"]
        expense_id, name, value, category, monthly, date = values

        edit_win = tk.Toplevel(window)
        edit_win.title("Επεξεργασία Εξόδου")
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
                main_app.edit_expense(
                    expense_id,
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

    tk.Button(btn_frame, text="Επεξεργασία", command=edit_expense).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Διαγραφή", command=delete_expense).pack(side="left", padx=10)

    load_data()

