from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import tkinter as tk
import matplotlib.pyplot as plt  # Για δημιουργία γραφημάτων

# Συνάρτηση δημιουργίας πίτας με έσοδα ανά κατηγορία, ενσωματωμένη σε περιβάλλον tkinter
def create_chart3(master, main_app):
    try:
        raw_data = main_app.get_income()  # Ανάκτηση εσόδων από την κύρια εφαρμογή
    except Exception as e:
        print(f"Σφάλμα κατά την ανάκτηση εισοδημάτων: {e}")
        raw_data = []

    # Εάν δεν υπάρχουν έσοδα, προσθέτουμε ένα προεπιλεγμένο dummy στοιχείο για να μην σπάσει η πίτα
    if not raw_data:
        raw_data = [(None, "Καμία Κατηγορία", 1.0, None, None, None)]

    # Δημιουργία χάρτη ID -> Όνομα Κατηγορίας
    category_map = {cat_id: name for cat_id, name in main_app.categories}

    # Άθροιση των εσόδων ανά κατηγορία
    income_by_category = defaultdict(float)
    for entry in raw_data:
        try:
            _, _, value, category_id, _, _ = entry
            category_name = category_map.get(category_id, "Άγνωστη Κατηγορία")
            income_by_category[category_name] += float(value)
        except Exception as e:
            print(f"Παράλειψη εγγραφής λόγω σφάλματος: {e}")
            continue

    # Παρασκευή δεδομένων για το γράφημα
    labels = list(income_by_category.keys())
    values = list(income_by_category.values())

    # Αν δεν υπάρχουν κατηγορίες, βάλε προεπιλεγμένες τιμές
    if not labels:
        labels = ["Καμία Κατηγορία"]
        values = [1.0]

    # Παλέτα χρωμάτων
    colors = ['#32a852', '#3298a8', '#a8a832', '#a83232', '#6632a8',
              '#2ecc71', '#9b59b6', '#f1c40f', '#e67e22', '#1abc9c']

    # Δημιουργία πίτας με matplotlib
    fig, ax = plt.subplots(dpi=100)
    ax.pie(
        values,
        labels=labels,
        colors=colors * ((len(values) // len(colors)) + 1),  # Επαναλαμβάνει τα χρώματα αν χρειάζεται
        autopct='%1.1f%%',  # Ποσοστά
        startangle=90,      # Αρχική γωνία
        shadow=True,        # Σκίαση
        radius=0.9          # Μέγεθος πίτας
    )
    ax.axis('equal')  # Ισομετρική πίτα
    plt.title("Έσοδα ανά Κατηγορία", loc='left')  # Τίτλος πίτας

    # Δημιουργία tkinter Frame που θα περιέχει το γράφημα
    container = tk.Frame(master)
    container.grid(row=0, column=0, sticky="nsew")  # Χρήση grid για καλύτερο έλεγχο διάταξης

    # Τοποθέτηση του γραφήματος (canvas) μέσα στο tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=0, sticky="nsew")  # Προσαρμόζεται στο μέγεθος του frame

    # Επιτρέπει στο γράφημα να αναπροσαρμόζεται όταν αλλάζει το μέγεθος του παραθύρου
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    return container  # Επιστρέφει το frame για περαιτέρω ενσωμάτωση




