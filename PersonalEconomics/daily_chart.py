from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import helpers

def daily_bar_chart(parent, main_instance, date):
    # Μορφοποίηση της ημερομηνίας (π.χ. σε YYYY-MM-DD)
    date = helpers.format_date(date)

    # Λήψη δεδομένων εσόδων και εξόδων για τη συγκεκριμένη ημερομηνία
    income_result = main_instance.get_incomes_by_date(date)
    expense_result = main_instance.get_expenses_by_date(date)

    # Υπολογισμός συνολικών ποσών
    income = sum(float(entry[2]) for entry in income_result['data']) if income_result['success'] else 0.0
    expenses = sum(float(entry[2]) for entry in expense_result['data']) if expense_result['success'] else 0.0

    # === Δημιουργία responsive frame για να τοποθετηθεί το γράφημα ===
    container = tk.Frame(parent)
    container.grid_rowconfigure(0, weight=1)      # Επιτρέπει την επέκταση της γραμμής
    container.grid_columnconfigure(0, weight=1)   # Επιτρέπει την επέκταση της στήλης

    # Δημιουργία αντικειμένου Figure για το γράφημα
    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)  # Προσθήκη υπο-γραφήματος (1x1, πρώτο)

    # Αν δεν υπάρχουν δεδομένα για την ημέρα, εμφάνιση μηνύματος
    if income == 0.0 and expenses == 0.0:
        ax.text(
            0.5, 0.5,
            "Δεν έγινε καμία\nσυναλλαγή τη\nσυγκεκριμένη ημερομηνία",
            ha='center', va='center',     # Κεντράρισμα κειμένου
            fontsize=9, color='gray',
            transform=ax.transAxes,       # Συντεταγμένες με βάση το γράφημα
            linespacing=1.5
        )
        ax.set_xticks([])  # Απόκρυψη του άξονα Χ
        ax.set_yticks([])  # Απόκρυψη του άξονα Υ
    else:
        # Αν υπάρχουν συναλλαγές, εμφάνιση bar chart
        ax.bar(["Έσοδα", "Έξοδα"], [income, expenses], color=["green", "red"])
        ax.set_ylabel("Ποσό (€)")  # Ετικέτα άξονα Υ

    # Τίτλος γραφήματος με ημερομηνία
    ax.set_title(f"Ημερήσια Σύνοψη\n({date})")

    # Ενσωμάτωση του matplotlib figure στο tkinter widget
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()

    # Απόκτηση widget και τοποθέτηση του με grid
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky="nsew")  # Κάλυψη όλου του container

    return container  # Επιστροφή του frame ώστε να μπορεί να προστεθεί στο UI


