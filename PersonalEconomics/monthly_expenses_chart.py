import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import tkinter as tk  # ΠΡΟΣΘΗΚΗ: Αν δεν υπάρχει ήδη

def create_chart1(master, main_app):
    expenses = main_app.get_expense()

    # Χάρτης κατηγορίας
    category_map = {cat[0]: cat[1] for cat in main_app.categories}

    # Ομαδοποίηση ποσών ανά όνομα κατηγορίας
    expense_by_category = defaultdict(float)
    for exp in expenses:
        category_id = exp[3]
        value = float(exp[2])
        category_name = category_map.get(category_id, "Άγνωστη Κατηγορία")
        expense_by_category[category_name] += value

    if not expense_by_category:
        expense_by_category["Κανένα Έξοδο"] = 1

    categories = list(expense_by_category.keys())
    num_euros = list(expense_by_category.values())

    fig, ax = plt.subplots(figsize=(5, 3), dpi=100)

    # Δημιουργία μπάρας
    bars = ax.bar(categories, num_euros, color='#a83232')

    ax.set_title("Μηνιαία Έξοδα ανά Κατηγορία", loc= 'left')
    ax.set_ylabel("Ευρώ")
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, rotation=30, ha='right')

    # Προσθήκη τιμών πάνω στις μπάρες
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}€',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    # Δημιουργία container
    container = tk.Frame(master)
    container.grid(row=0, column=0, sticky='nsew')  # ή .pack() αν προτιμάς

    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    return container

