import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from models.income import Income
from datetime import datetime
from category_manager import open_category_manager
from helpers import refresh_all_charts


income_window_ref = None  # Για αποφυγή διπλού ανοίγματος παραθύρου


def submit_income(main_app, name, amount, category_id, date, is_recurring):
    try:
        value = float(amount)
    except ValueError:
        messagebox.showerror("Σφάλμα", "Το ποσό πρέπει να είναι αριθμός.")
        return

    # ✅ Διορθωμένη μετατροπή ημερομηνίας
    if isinstance(date, str):
        try:
            date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            pass

    income = Income(
        name=name,
        value=value,
        category=category_id,
        monthly=is_recurring,
        date=date
    )

    try:
        res = main_app.add_income(income)
        if not res["success"]:
            msg = '\n'.join(res['errors'])
            messagebox.showerror(
                "Error",  msg)
            return
        main_app.refresh_chart1()
        print(
            f"✅ Καταχωρήθηκε: {value}€ - Κατηγορία ID {category_id} - {date}")
        messagebox.showinfo("Επιτυχία", "To έσοδο καταχωρήθηκε με επιτυχία!")

    except Exception as e:
        messagebox.showerror("Σφάλμα", str(e))


def open_incomes_window(main_app):
    global income_window_ref

    if income_window_ref is not None and income_window_ref.winfo_exists():
        income_window_ref.lift()
        return

    income_window = tk.Toplevel()
    income_window_ref = income_window
    income_window.title("Καταχώρηση Εσόδου")
    income_window.configure(bg="white")

    tk.Label(income_window, text="Καταχώρηση νέου εσόδου", font=(
        "Arial", 16, "bold"), bg="white").pack(anchor='nw', padx=20, pady=15)

    tk.Label(income_window, text="Ονομα:",
             bg="white").pack(anchor='nw', padx=20)
    name_var = tk.StringVar()
    name_entry = ttk.Entry(income_window, textvariable=name_var)
    name_entry.pack(anchor='nw', padx=20, pady=5)
    tk.Label(income_window, text="Ποσό (€):",
             bg="white").pack(anchor='nw', padx=20)
    amount_var = tk.StringVar()
    amount_entry = ttk.Combobox(income_window, values=[
                                "10", "20", "50", "100"], textvariable=amount_var)
    amount_entry['state'] = 'normal'
    amount_entry.pack(anchor='nw', padx=20, pady=5)

    tk.Label(income_window, text="Κατηγορία:",
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
        income_window, values=category_names, textvariable=category_var)
    category_entry.pack(anchor='nw', padx=20, pady=5)

    def on_category_select(event):
        if category_var.get() == "➕ Διαχείριση κατηγοριών":
            open_category_manager(main_app, refresh_categories)
            category_var.set("")

    category_entry.bind("<<ComboboxSelected>>", on_category_select)

    tk.Label(income_window, text="Ημερομηνία:", bg="white").pack(
        anchor='nw', padx=20, pady=(10, 0))
    cal = Calendar(income_window, selectmode='day', date_pattern='yyyy-mm-dd')
    cal.pack(anchor='nw', padx=20, pady=5)

    is_recurring_var = tk.BooleanVar()
    recurring_check = tk.Checkbutton(
        income_window, text="Καταχώρηση ως μηνιαία", variable=is_recurring_var, bg="white")
    recurring_check.pack(anchor='nw', padx=20, pady=10)

    from helpers import refresh_all_charts  # Βάλε το στην αρχή του αρχείου (αν δεν υπάρχει ήδη)

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

        submit_income(main_app, name, amount, category_id, date, is_recurring)

        refresh_all_charts(main_app)

        income_window.destroy()

    submit_btn = tk.Button(income_window, text="Υποβολή", command=on_submit)
    submit_btn.pack(anchor='nw', padx=20, pady=10)
    def on_close():
        global income_window_ref
        income_window_ref = None
        income_window.destroy()

    income_window.protocol("WM_DELETE_WINDOW", on_close)
