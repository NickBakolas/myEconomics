import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from models.expense import Expense
from datetime import datetime
from category_manager import open_category_manager
from helpers import refresh_all_charts


expense_window_ref = None  # Για αποφυγή διπλού ανοίγματος παραθύρου


def submit_expense(main_app, name, amount, category_id, date, is_recurring):
    try:
        value = float(amount)
    except ValueError:
        messagebox.showerror("Σφάλμα", "Το ποσό πρέπει να είναι αριθμός.")
        return

    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass

    expense = Expense(
        name=name,
        value=value,
        category=category_id,
        monthly=is_recurring,
        date=date
    )

    try:
        res = main_app.add_expense(expense)
        if not res["success"]:
            msg = '\n'.join(res['errors'])
            messagebox.showerror(
                "Error",  msg)
            return
        main_app.refresh_chart1()
        print(
            f"✅ Καταχωρήθηκε: {value}€ - Κατηγορία ID {category_id} - {date}")
        messagebox.showinfo(
            "Επιτυχία", "Η δαπάνη καταχωρήθηκε με επιτυχία!")

    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))


def open_expense_window(main_app):
    global expense_window_ref

    if expense_window_ref is not None and expense_window_ref.winfo_exists():
        expense_window_ref.lift()
        return

    expense_window = tk.Toplevel()
    expense_window_ref = expense_window
    expense_window.title("Καταχώρηση Δαπάνης")
    expense_window.configure(bg="white")


    tk.Label(expense_window, text="Καταχώρηση νέας δαπάνης", font=(
        "Arial", 16, "bold"), bg="white").pack(anchor='nw', padx=20, pady=15)

    tk.Label(expense_window, text="Ονομα:",
             bg="white").pack(anchor='nw', padx=20)
    name_var = tk.StringVar()
    name_entry = ttk.Entry(expense_window, textvariable=name_var)
    name_entry.pack(anchor='nw', padx=20, pady=5)
    tk.Label(expense_window, text="Ποσό (€):",
             bg="white").pack(anchor='nw', padx=20)
    amount_var = tk.StringVar()
    amount_entry = ttk.Combobox(expense_window, values=[
                                "10", "20", "50", "100"], textvariable=amount_var)
    amount_entry['state'] = 'normal'
    amount_entry.pack(anchor='nw', padx=20, pady=5)

    tk.Label(expense_window, text="Κατηγορία:",
             bg="white").pack(anchor='nw', padx=20)
    category_var = tk.StringVar()

    def refresh_categories():
        nonlocal categories
        categories = main_app.categories
        names = [cat[1] for cat in categories] + ["➕ Διαχείριση κατηγοριών"]
        category_entry['values'] = names

    categories = main_app.categories
    category_names = [cat[1]
                      for cat in categories] + ["➕ Διαχείριση κατηγοριών"]
    category_entry = ttk.Combobox(
        expense_window, values=category_names, textvariable=category_var)
    category_entry.pack(anchor='nw', padx=20, pady=5)

    def on_category_select(event):
        if category_var.get() == "➕ Διαχείριση κατηγοριών":
            open_category_manager(main_app, refresh_categories)
            category_var.set("")

    category_entry.bind("<<ComboboxSelected>>", on_category_select)

    tk.Label(expense_window, text="Ημερομηνία:", bg="white").pack(
        anchor='nw', padx=20, pady=(10, 0))
    cal = Calendar(expense_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(anchor='nw', padx=20, pady=5)

    is_recurring_var = tk.BooleanVar()
    recurring_check = tk.Checkbutton(
        expense_window, text="Καταχώρηση ως μηνιαία", variable=is_recurring_var, bg="white")
    recurring_check.pack(anchor='nw', padx=20, pady=10)

    def on_submit():
        amount = amount_var.get().strip()
        name = name_var.get().strip()
        category_name = category_var.get().strip()
        date = cal.get_date()
        is_recurring = is_recurring_var.get()

        category_id = next(
            (cat[0] for cat in categories if cat[1] == category_name), None)

        if not amount or not category_id:
            messagebox.showwarning("Σφάλμα", "Συμπληρώστε όλα τα πεδία.")
            return

        submit_expense(main_app, name,  amount, category_id, date, is_recurring)

        refresh_all_charts(main_app)

        expense_window.destroy()

    submit_btn = tk.Button(expense_window, text="Υποβολή", command=on_submit)
    submit_btn.pack(anchor='nw', padx=20, pady=10)

    def on_close():
        global expense_window_ref
        expense_window_ref = None
        expense_window.destroy()

    expense_window.protocol("WM_DELETE_WINDOW", on_close)
