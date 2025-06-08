import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
from models.expense import Expense
from category_manager import open_category_manager
from helpers import refresh_all_charts
from PIL import Image, ImageTk

# Μεταβλητή αναφοράς στο παράθυρο, ώστε να μην ανοίγει δεύτερη φορά
expense_window_ref = None


def submit_expense(main_app, name, amount, category_id, date, is_recurring):
    """
    Δημιουργεί και προσθέτει μια νέα δαπάνη στην εφαρμογή.
    Περιλαμβάνει έλεγχο εγκυρότητας ποσού και μορφής ημερομηνίας.
    """
    try:
        value = float(amount)  # Μετατροπή του ποσού σε float
    except ValueError:
        messagebox.showerror("Σφάλμα", "Το ποσό πρέπει να είναι αριθμός.")
        return

    # Αν η ημερομηνία είναι σε μορφή string, μετατρέπεται στο κατάλληλο format
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass  # Αν είναι ήδη σε σωστή μορφή, την αφήνουμε ως έχει

    # Δημιουργία αντικειμένου Expense
    expense = Expense(
        name=name,
        value=value,
        category=category_id,
        monthly=is_recurring,
        date=date
    )

    # Προσθήκη δαπάνης μέσω της κύριας εφαρμογής
    try:
        res = main_app.add_expense(expense)
        if not res["success"]:
            messagebox.showerror("Σφάλμα", '\n'.join(res['errors']))
            return
        messagebox.showinfo("Επιτυχία", "Η δαπάνη καταχωρήθηκε με επιτυχία!")
    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))


def open_expense_window(main_app):
    """
    Δημιουργεί και εμφανίζει το παράθυρο καταχώρησης νέας δαπάνης.
    Προσθέτει πεδία για όνομα, ποσό, κατηγορία, ημερομηνία και μηνιαία σήμανση.
    """
    global expense_window_ref

    # Αν το παράθυρο είναι ήδη ανοιχτό, το φέρνουμε στο προσκήνιο
    if expense_window_ref and expense_window_ref.winfo_exists():
        expense_window_ref.lift()
        return

    # Δημιουργία νέου παραθύρου
    expense_window = tk.Toplevel()
    expense_window.grab_set()  # Κάνε το παράθυρο modal
    expense_window_ref = expense_window
    expense_window.title("Καταχώρηση Δαπάνης")
    expense_window.configure(bg="white")

    # Ορισμός εικονιδίου παραθύρου
    icon_path = "assets/expense.png"
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    expense_window.iconphoto(False, icon_photo)

    # Επικεφαλίδα
    tk.Label(expense_window, text="Καταχώρηση νέας δαπάνης", font=("Arial", 16, "bold"), bg="white").pack(anchor='nw', padx=20, pady=15)

    # Πεδία εισαγωγής
    tk.Label(expense_window, text="Περιγραφή:", bg="white").pack(anchor='nw', padx=20)
    name_var = tk.StringVar()
    ttk.Entry(expense_window, textvariable=name_var).pack(anchor='nw', padx=20, pady=5)

    tk.Label(expense_window, text="Ποσό (€):", bg="white").pack(anchor='nw', padx=20)
    amount_var = tk.StringVar()
    ttk.Combobox(expense_window, values=["10", "20", "50", "100"], textvariable=amount_var, state='normal').pack(anchor='nw', padx=20, pady=5)

    # Επιλογή Κατηγορίας
    tk.Label(expense_window, text="Κατηγορία:", bg="white").pack(anchor='nw', padx=20)
    category_var = tk.StringVar()
    category_entry = ttk.Combobox(expense_window, textvariable=category_var)
    category_entry.pack(anchor='nw', padx=20, pady=5)

    # Ενημέρωση διαθέσιμων κατηγοριών
    def refresh_categories():
        categories = main_app.categories
        category_entry['values'] = [cat[1] for cat in categories] + ["➕ Διαχείριση κατηγοριών"]

    refresh_categories()  # Αρχική φόρτωση των κατηγοριών

    # Άνοιγμα παραθύρου διαχείρισης κατηγοριών αν επιλεγεί η ειδική επιλογή
    def on_category_select(event):
        if category_var.get() == "➕ Διαχείριση κατηγοριών":
            open_category_manager(main_app, refresh_categories)
            category_var.set("")  # Καθαρισμός πεδίου

    category_entry.bind("<<ComboboxSelected>>", on_category_select)

    # Ημερολόγιο επιλογής ημερομηνίας
    tk.Label(expense_window, text="Ημερομηνία:", bg="white").pack(anchor='nw', padx=20, pady=(10, 0))
    cal = Calendar(expense_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(anchor='nw', padx=20, pady=5)

    # Επιλογή για επαναλαμβανόμενη δαπάνη
    is_recurring_var = tk.BooleanVar()
    tk.Checkbutton(expense_window, text="Καταχώρηση ως μηνιαία", variable=is_recurring_var, bg="white").pack(anchor='nw', padx=20, pady=10)

    # Ενέργεια Υποβολής
    def on_submit():
        name = name_var.get().strip()
        amount = amount_var.get().strip()
        category_name = category_var.get().strip()
        date = cal.get_date()
        is_recurring = is_recurring_var.get()

        # Εύρεση ID κατηγορίας με βάση το όνομα
        category_id = next((cat[0] for cat in main_app.categories if cat[1] == category_name), None)

        # Έλεγχος αν έχουν συμπληρωθεί τα απαραίτητα πεδία
        if not amount or not category_id:
            messagebox.showwarning("Σφάλμα", "Συμπληρώστε όλα τα πεδία.")
            return

        # Καταχώρηση της δαπάνης
        submit_expense(main_app, name, amount, category_id, date, is_recurring)
        refresh_all_charts(main_app)  # Ενημέρωση γραφημάτων
        expense_window.destroy()  # Κλείσιμο παραθύρου

    # Κουμπί Υποβολής
    tk.Button(expense_window, text="Υποβολή", command=on_submit).pack(anchor='nw', padx=20, pady=10)

    # Διαχείριση κλεισίματος παραθύρου
    def on_close():
        global expense_window_ref
        expense_window_ref = None  # Καθαρισμός αναφοράς
        expense_window.destroy()

    expense_window.protocol("WM_DELETE_WINDOW", on_close)

