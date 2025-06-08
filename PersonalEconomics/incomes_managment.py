import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

income_window_ref = None  # Αναφορά στο κύριο παράθυρο εσόδων για αποφυγή πολλαπλού ανοίγματος
edit_income_win_ref = None  # Αναφορά στο παράθυρο επεξεργασίας εσόδου για αποφυγή διπλού ανοίγματος

def open_incomes_details_window(main_app):
    global income_window_ref, edit_income_win_ref

    # Αν το παράθυρο είναι ήδη ανοιχτό, το φέρνει μπροστά
    if income_window_ref is not None and income_window_ref.winfo_exists():
        income_window_ref.lift()
        income_window_ref.focus_force()
        return

    # Δημιουργία νέου παραθύρου
    income_window_ref = tk.Toplevel()
    income_window_ref.grab_set()
    window = income_window_ref
    window.title("Λίστα Εσόδων")
    window.geometry("800x400")  # Διαστάσεις παραθύρου

    # Φόρτωση και εμφάνιση εικονιδίου παραθύρου
    icon_path = "assets/income.png"
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    window.iconphoto(False, icon_photo)

    # Συνάρτηση που τρέχει όταν το παράθυρο κλείνει
    def on_close():
        global income_window_ref
        income_window_ref = None
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_close)

    # Δημιουργία λεξικών για εύκολη αντιστοίχιση κατηγοριών
    category_map = {cat_id: name for cat_id, name in main_app.categories}
    reverse_category_map = {name: cat_id for cat_id, name in main_app.categories}
    category_names = list(reverse_category_map.keys())

    # Δημιουργία Treeview για εμφάνιση των εσόδων
    tree = ttk.Treeview(window, columns=("id", "name", "value", "category", "monthly", "date"), show="headings")
    for col, text in zip(tree["columns"], ["ID", "Περιγραφή", "Ποσό", "Κατηγορία", "Μηνιαίο", "Ημερομηνία"]):
        tree.heading(col, text=text)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Φόρτωση δεδομένων στη λίστα
    def load_data():
        tree.delete(*tree.get_children())  # Καθαρισμός προηγούμενων δεδομένων
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

    # Διαγραφή επιλεγμένου εσόδου
    def delete_income():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return
        income_id = tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Επιβεβαίωση", f"Διαγραφή εσόδου με ID {income_id};"):
            try:
                main_app.delete_income(income_id)
                load_data()
                main_app.refresh_all_charts()
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Σφάλμα διαγραφής: {e}")

    # Επεξεργασία επιλεγμένου εσόδου
    def edit_income():
        global edit_income_win_ref

        # Αν το παράθυρο επεξεργασίας είναι ήδη ανοιχτό, το φέρνει μπροστά
        if edit_income_win_ref is not None and edit_income_win_ref.winfo_exists():
            edit_income_win_ref.lift()
            edit_income_win_ref.focus_force()
            return

        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return

        # Λήψη δεδομένων από την επιλεγμένη εγγραφή
        values = tree.item(selected[0])["values"]
        income_id, name, value, category, monthly, date = values

        # Δημιουργία παραθύρου επεξεργασίας
        edit_win = tk.Toplevel(window)
        edit_income_win_ref = edit_win
        edit_win.title("Επεξεργασία Εσόδου")
        edit_win.geometry("350x350")

        # Φόρτωση εικονιδίου για το παράθυρο επεξεργασίας
        icon_path = "assets/income.png"
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        edit_win.iconphoto(False, icon_photo)

        # Συνάρτηση για το κλείσιμο του παραθύρου επεξεργασίας
        def on_close_edit():
            global edit_income_win_ref
            edit_income_win_ref = None
            edit_win.destroy()

        edit_win.protocol("WM_DELETE_WINDOW", on_close_edit)

        # Πεδίο περιγραφής
        tk.Label(edit_win, text="Περιγραφή").pack()
        name_entry = tk.Entry(edit_win)
        name_entry.insert(0, name)
        name_entry.pack()

        # Πεδίο ποσού
        tk.Label(edit_win, text="Ποσό").pack()
        value_entry = tk.Entry(edit_win)
        value_entry.insert(0, str(value))
        value_entry.pack()

        # Πεδίο ημερομηνίας (ως Entry)
        tk.Label(edit_win, text="Ημερομηνία").pack()
        date_entry = tk.Entry(edit_win)
        date_entry.insert(0, date)
        date_entry.pack()

        # Επιλογή κατηγορίας (ComboBox)
        tk.Label(edit_win, text="Κατηγορία").pack()
        category_combo = ttk.Combobox(edit_win, values=category_names, state="readonly")
        category_combo.set(category)
        category_combo.pack()

        # Επιλογή αν είναι μηνιαίο
        monthly_var = tk.BooleanVar(value=(monthly == "Ναι"))
        tk.Checkbutton(edit_win, text="Μηνιαίο", variable=monthly_var).pack(pady=5)

        # Αποθήκευση αλλαγών
        def save_changes():
            global edit_income_win_ref
            try:
                new_category_name = category_combo.get()
                if new_category_name not in reverse_category_map:
                    raise ValueError("Μη έγκυρη κατηγορία.")

                main_app.edit_income(
                    income_id,
                    name=name_entry.get(),
                    value=float(value_entry.get()),
                    date=date_entry.get(),
                    category=new_category_name,
                    monthly=monthly_var.get()
                )
                edit_win.destroy()
                edit_income_win_ref = None
                load_data()
                main_app.refresh_all_charts()
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Αποτυχία αποθήκευσης αλλαγών: {e}")

        # Κουμπί αποθήκευσης
        tk.Button(edit_win, text="Αποθήκευση", command=save_changes).pack(pady=10)

    # Πλαίσιο με κουμπιά κάτω από τη λίστα
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=5)

    # Κουμπιά επεξεργασίας και διαγραφής
    tk.Button(btn_frame, text="Επεξεργασία", command=edit_income).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Διαγραφή", command=delete_income).pack(side="left", padx=10)

    # Αρχική φόρτωση δεδομένων
    load_data()



