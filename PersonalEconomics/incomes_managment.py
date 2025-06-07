import tkinter as tk
from tkinter import ttk, messagebox

# Χρησιμοποιείται για να διατηρείται αναφορά στο παράθυρο και να αποφεύγεται το άνοιγμα πολλών παραθύρων ταυτόχρονα
income_window_ref = None

def open_income_details_window(main_app):
    global income_window_ref

    # Αν το παράθυρο είναι ήδη ανοιχτό, το φέρνουμε μπροστά
    if income_window_ref is not None and income_window_ref.winfo_exists():
        income_window_ref.lift()
        income_window_ref.focus_force()
        return

    # Δημιουργία νέου παραθύρου για εμφάνιση των εσόδων
    income_window_ref = tk.Toplevel()
    window = income_window_ref
    window.title("Λίστα Εσόδων")
    window.geometry("800x400")

    # Συνάρτηση για σωστό χειρισμό κλεισίματος παραθύρου
    def on_close():
        global income_window_ref
        income_window_ref = None  # Μηδενίζουμε την αναφορά
        window.destroy()

    # Ορίζουμε την παραπάνω συνάρτηση ως handler όταν κλείνει το παράθυρο
    window.protocol("WM_DELETE_WINDOW", on_close)

    # Δημιουργία χάρτη κατηγοριών με βάση το main_app (id -> name)
    category_map = {cat_id: name for cat_id, name in main_app.categories}

    # Δημιουργία Treeview για την απεικόνιση των εσόδων
    tree = ttk.Treeview(window, columns=("id", "name", "value", "category", "monthly", "date"), show="headings")
    for col, text in zip(tree["columns"], ["ID", "Περιγραφή", "Ποσό", "Κατηγορία", "Μηνιαίο", "Ημερομηνία"]):
        tree.heading(col, text=text)
        tree.column(col, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Συνάρτηση για φόρτωση των δεδομένων στον πίνακα
    def load_data():
        tree.delete(*tree.get_children())  # Καθαρισμός υπάρχοντων γραμμών
        try:
            data = main_app.get_income()  # Λήψη λίστας εσόδων από το κύριο πρόγραμμα
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία φόρτωσης εσόδων: {e}")
            return
        for row in data:
            id_, name, value, cat_id, monthly, date = row
            category = category_map.get(cat_id, "Άγνωστη")
            monthly_text = "Ναι" if monthly else "Όχι"
            tree.insert("", "end", values=(id_, name, value, category, monthly_text, date))

    # Συνάρτηση για διαγραφή επιλεγμένου εισοδήματος
    def delete_income():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return
        income_id = tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Επιβεβαίωση", f"Διαγραφή εισοδήματος με ID {income_id};"):
            try:
                main_app.delete_income(income_id)
                load_data()  # Ανανεώνουμε τα δεδομένα
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Σφάλμα διαγραφής: {e}")

    # Συνάρτηση για επεξεργασία επιλεγμένου εισοδήματος
    def edit_income():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Επιλογή", "Επιλέξτε μια εγγραφή.")
            return
        values = tree.item(selected[0])["values"]
        income_id, name, value, category, monthly, date = values

        # Δημιουργία παραθύρου επεξεργασίας
        edit_win = tk.Toplevel(window)
        edit_win.title("Επεξεργασία Εισοδήματος")
        edit_win.geometry("350x300")

        # Πεδία εισαγωγής δεδομένων
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

        # Επιλογή αν είναι μηνιαίο
        monthly_var = tk.BooleanVar(value=(monthly == "Ναι"))
        tk.Checkbutton(edit_win, text="Μηνιαίο", variable=monthly_var).pack(pady=5)

        # Αποθήκευση αλλαγών
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
                load_data()  # Επαναφόρτωση με τις αλλαγές
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Αποτυχία αποθήκευσης αλλαγών: {e}")

        tk.Button(edit_win, text="Αποθήκευση", command=save_changes).pack(pady=10)

    # Πλαίσιο κουμπιών στο κάτω μέρος
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=5)

    # Κουμπιά για επεξεργασία και διαγραφή
    tk.Button(btn_frame, text="Επεξεργασία", command=edit_income).pack(side="left", padx=10)
    tk.Button(btn_frame, text="Διαγραφή", command=delete_income).pack(side="left", padx=10)

    # Αρχική φόρτωση των δεδομένων
    load_data()

