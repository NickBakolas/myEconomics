import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_chart2(master, main_app):
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    months_labels = ['Ιαν', 'Φεβρ', 'Μάρτ', 'Απρ', 'Μαι',
                     'Ιούν', 'Ιούλ', 'Αύγ', 'Σεπτ', 'Οκτ', 'Νοέ', 'Δεκ']
    income_data = [0.0] * 12
    expense_data = [0.0] * 12

    try:
        income_raw = main_app.get_incomes_per_month()
        expense_raw = main_app.get_expenses_per_month()

        for month_str, value in income_raw:
            index = int(month_str) - 1
            income_data[index] = value

        for month_str, value in expense_raw:
            index = int(month_str) - 1
            expense_data[index] = value

    except Exception as e:
        print(f"Σφάλμα φόρτωσης δεδομένων: {e}")

    ax.plot(months_labels, income_data, color='#44f205',
            linestyle='solid', label='Έσοδα')
    ax.plot(months_labels, expense_data, color='#f20505',
            linestyle='solid', label='Έξοδα')

    ax.set_title("Σταθερά Έσοδα - Έξοδα ανά Μήνα")
    ax.set_ylabel("Ευρώ")
    ax.legend(loc='upper center')

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    return canvas.get_tk_widget()
