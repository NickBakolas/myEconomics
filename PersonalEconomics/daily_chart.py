from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import helpers as helpers

def daily_bar_chart(parent, main_instance, date):
    date = helpers.format_date(date)

    income_result = main_instance.get_incomes_by_date(date)
    expense_result = main_instance.get_expenses_by_date(date)

    income = sum(float(entry[2]) for entry in income_result['data']) if income_result['success'] else 0.0
    expenses = sum(float(entry[2]) for entry in expense_result['data']) if expense_result['success'] else 0.0

    # === Δημιουργία responsive container ===
    container = tk.Frame(parent)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    fig = Figure(figsize=(4, 3), dpi=100)
    ax = fig.add_subplot(111)

    if income == 0.0 and expenses == 0.0:
        ax.text(
            0.5, 0.5,
            "Δεν έγινε καμία\nσυναλλαγή τη\nσυγκεκριμένη ημερομηνία",
            ha='center', va='center',
            fontsize=9, color='gray',
            transform=ax.transAxes,
            linespacing=1.5
        )
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        ax.bar(["Έσοδα", "Έξοδα"], [income, expenses], color=["green", "red"])
        ax.set_ylabel("Ποσό (€)")

    ax.set_title(f"Ημερήσια Σύνοψη\n({date})")

    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()

    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky="nsew")  # ✅ Χρήση grid με sticky

    return container

