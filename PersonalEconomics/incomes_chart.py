from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import tkinter as tk
import matplotlib.pyplot as plt  # Μην ξεχνάς αυτό

def create_chart3(master, main_app):
    try:
        raw_data = main_app.get_income()
    except Exception as e:
        print(f"Σφάλμα κατά την ανάκτηση εισοδημάτων: {e}")
        raw_data = []

    if not raw_data:
        raw_data = [(None, "Καμία Κατηγορία", 1.0, None, None, None)]

    category_map = {cat_id: name for cat_id, name in main_app.categories}

    income_by_category = defaultdict(float)
    for entry in raw_data:
        try:
            _, _, value, category_id, _, _ = entry
            category_name = category_map.get(category_id, "Άγνωστη Κατηγορία")
            income_by_category[category_name] += float(value)
        except Exception as e:
            print(f"Παράλειψη εγγραφής λόγω σφάλματος: {e}")
            continue

    labels = list(income_by_category.keys())
    values = list(income_by_category.values())

    if not labels:
        labels = ["Καμία Κατηγορία"]
        values = [1.0]

    colors = ['#32a852', '#3298a8', '#a8a832', '#a83232', '#6632a8',
              '#2ecc71', '#9b59b6', '#f1c40f', '#e67e22', '#1abc9c']

    fig, ax = plt.subplots(dpi=100)
    ax.pie(values,
           labels=labels,
           colors=colors * ((len(values) // len(colors)) + 1),
           autopct='%1.1f%%',
           startangle=90,
           shadow=True,
           radius=0.9)
    ax.axis('equal')
    plt.title("Έσοδα ανά Κατηγορία", loc='left')

    # Container με χρήση grid (αντί για pack)
    container = tk.Frame(master)
    container.grid(row=0, column=0, sticky="nsew")

    # Προσαρμογή canvas με χρήση grid
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky="nsew")

    # Ενεργοποίηση αναπροσαρμογής χώρου
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    return container




