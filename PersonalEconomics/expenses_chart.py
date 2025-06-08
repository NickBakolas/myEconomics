import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import tkinter as tk

# Συνάρτηση για τη δημιουργία του γραφήματος εξόδων ανά κατηγορία
def create_chart1(master, main_app):
    # Λήψη όλων των εξόδων από το κύριο app
    expenses = main_app.get_expense()

    # Δημιουργία λεξικού που αντιστοιχεί τα ID των κατηγοριών με τα ονόματά τους
    category_map = {cat_id: name for cat_id, name in main_app.categories}

    # Χρήση defaultdict για την ομαδοποίηση των εξόδων ανά κατηγορία
    expense_by_category = defaultdict(float)
    for exp in expenses:
        try:
            value = float(exp[2])         # Το ποσό του εξόδου
            category_id = exp[3]          # Το ID της κατηγορίας
            category_name = category_map.get(category_id, "Άγνωστη Κατηγορία")
            expense_by_category[category_name] += value
        except Exception as e:
            print(f"Σφάλμα επεξεργασίας εξόδου: {e}")  # Χειρισμός πιθανών σφαλμάτων

    # Εάν δεν υπάρχουν καθόλου έξοδα, δημιουργούμε εικονικό δεδομένο
    if not expense_by_category:
        expense_by_category["Κανένα Έξοδο"] = 1.0

    # Λίστες με τις κατηγορίες και τα αντίστοιχα ποσά
    categories = list(expense_by_category.keys())
    num_euros = list(expense_by_category.values())

    # Δημιουργία του διαγράμματος με matplotlib
    fig, ax = plt.subplots(dpi=100)
    bars = ax.bar(categories, num_euros, color='#a83232')  # Κόκκινες μπάρες
    ax.set_title("Έξοδα ανά Κατηγορία", loc='left')        # Τίτλος γραφήματος
    ax.set_ylabel("Ευρώ")                                  # Ετικέτα άξονα Υ
    ax.set_xticks(range(len(categories)))                  # Σημεία στον Χ άξονα
    ax.set_xticklabels(categories, rotation=20, ha='right')  # Ονόματα κατηγοριών

    # Εμφάνιση τιμών πάνω από κάθε μπάρα
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}€',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    # Δημιουργία frame (πλαίσιο) στο tkinter GUI
    container = tk.Frame(master)
    container.grid(row=0, column=0, sticky="nsew")

    # Ενσωμάτωση του γραφήματος στο tkinter με FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # Επιτρέπουμε στο container να μεγαλώνει με το παράθυρο
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    return container  # Επιστροφή του frame για χρήση στο GUI


