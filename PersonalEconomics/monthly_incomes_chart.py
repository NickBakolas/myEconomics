import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

def create_chart3(master, main_app):
    try:
        raw_data = main_app.get_income()
    except Exception as e:
        print(f"Σφάλμα κατά την ανάκτηση εισοδημάτων: {e}")
        raw_data = []

    if not raw_data:
        raw_data = [(None, "Καμία Κατηγορία", 1.0, None, None, None)]

    # Χάρτης id -> όνομα κατηγορίας
    category_map = {cat_id: name for cat_id, name in main_app.categories}

    # Ομαδοποίηση εισοδημάτων
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

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.pie(values,
           labels=labels,
           colors=colors * (len(values) // len(colors) + 1),
           autopct='%1.1f%%',
           startangle=90,
           shadow=True,
           radius=0.9)  # Προαιρετική μικρή μείωση ακτίνας
    ax.axis('equal')
    plt.title("Έσοδα ανά Κατηγορία")

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    return canvas.get_tk_widget()








