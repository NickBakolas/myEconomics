import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Μεταβλητή αναφοράς για αποφυγή διπλού ανοίγματος του παραθύρου
expense_window_ref = None

def open_expenses_details_window(main_app):
    """
    Άνοιγμα παραθύρου με λίστα εξόδων και δυνατότητα επεξεργασίας/διαγραφής.
    """
    global expense_window_ref

    # Αν το παράθυρο είναι ήδη ανοιχτό, το φέρνουμε στο προσκήνιο
    if expense_window_ref is not None and expense_window_ref.winfo_exists():
        expense_window_ref.lift()
        expense_window_ref.focus_force()
        return

    # Δημιουργία νέου παραθύρου
    expense_window_ref = tk.Toplevel()
    expense_window_ref.grab_set()
    window = expense_window_ref
    window.title("Λίστα Δαπανών")
    window.geometry("800x400")

    # Εικονίδιο παραθύρου
    icon_path = "assets/expense.png"
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    window.iconphoto(False, icon_photo)

    # Διαχείριση κλεισίματος παραθύρου
    def on_close():
        global expense_window_ref
        expense_window_ref = None
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    # Δημιουργία λεξικών για αντιστοίχιση κατηγορίας <-> ID
    category_map = {cat_id: name for cat_id, name in main_app.categories}
    reverse_category_map = {name: cat_id for cat_id, name in main_app.categories}
    category_names = list(reverse_category_map.keys())

    # Treeview για εμφάνιση εξόδων
    tree = ttk.Treeview(window, columns=("id", "name", "value", "category", "monthly", "date"), show="headings")
    for col, text in zip(tree["columns"], ["ID", "Περιγραφή", "Ποσό", "Κατηγορία", "Μηνιαίο", "Ημερομηνία"]):
        tree.heading(col, text=text)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Συνάρτηση φόρτωσης δεδομένων στον πίνακα
    def load_data():
        tree.delete(*tree.get_children())  # Καθαρισμός πίνακα
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

    # Συνάρτηση διαγραφής εξόδου
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
                main_app.refresh_all_charts()
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Σφάλμα διαγραφής: {e}")

    # === Μεταβλητή αναφοράς για παράθυρο επεξεργασίας ===
    edit_expense_win_ref = None

    # Συνάρτηση επεξεργασίας εξόδου
    def edit_expense():
        nonlocal edit_expense_win_ref

        # Αν υπάρχει ήδη παράθυρο επεξεργασίας, φέρτο μπροστά
        if edit_expense_win_ref is not None and edit_expense_win_ref.winfo_exists():
            edit_expense_win_ref.lift()
            edit_expense_win_ref.focus_force()
            return

        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return

        # Ανάκτηση τιμών από επιλεγμένη εγγραφή
        values = tree.item(selected[0])["values"]
        expense_id, name, value, category, monthly, date = values

        # Δημιουργία παραθύρου επεξεργασίας
        edit_win = tk.Toplevel(window)
        edit_expense_win_ref = edit_win
        edit_win.title("Επεξεργασία Εξόδου")
        edit_win.geometry("350x350")

        # Εικονίδιο
        icon_path = "assets/expense.png"
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        edit_win.iconphoto(False, icon_photo)

        # Διαχείριση κλεισίματος
        def on_close_edit():
            nonlocal edit_expense_win_ref
            edit_expense_win_ref = None
            edit_win.destroy()

        edit_win.protocol("WM_DELETE_WINDOW", on_close_edit)

        # === Πεδία επεξεργασίας ===
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

        tk.Label(edit_win, text="Κατηγορία").pack()
        category_combo = ttk.Combobox(edit_win, values=category_names, state="readonly")
        category_combo.set(category)
        category_combo.pack()

        # Checkbox για "μηνιαίο"
        monthly_var = tk.BooleanVar(value=(monthly == "Ναι"))
        tk.Checkbutton(edit_win, text="Μηνιαίο", variable=monthly_var).pack(pady=5)

        # Συνάρτηση αποθήκευσης αλλαγών
        def save_changes():
            try:
                new_category_name = category_combo.get()
                if new_category_name not in reverse_category_map:
                    raise ValueError("Μη έγκυρη κατηγορία.")

                # Ενημέρωση μέσω main_app
                main_app.edit_expense(
                    expense_id,
                    name=name_entry.get(),
                    value=float(value_entry.get()),
                    date=date_entry.get(),
                    category=new_category_name,
                    monthly=monthly_var.get()
                )
                edit_win.destroy()
                edit_expense_win_ref = None
                load_data()
                main_app.refresh_all_charts()
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Αποτυχία αποθήκευσης αλλαγών: {e}")

        # Κουμπί αποθήκευσης
        tk.Button(edit_win, text="Αποθήκευση", command=save_changes).pack(pady=10)

    # === Κουμπιά επεξεργασίας/διαγραφής ===
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Επεξεργασία", command=edit_expense).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Διαγραφή", command=delete_expense).pack(side="left", padx=10)

    # Αρχική φόρτωση δεδομένων
    load_data()



