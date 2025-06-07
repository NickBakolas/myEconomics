import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_chart2(master, main_app):
    # Δημιουργία figure και axis για το διάγραμμα με ανάλυση 100 dpi
    fig, ax = plt.subplots(dpi=100)

    # Ετικέτες μηνών στα ελληνικά (Ιανουάριος έως Δεκέμβριος)
    months_labels = ['Ιαν', 'Φεβρ', 'Μάρτ', 'Απρ', 'Μαι', 'Ιούν',
                     'Ιούλ', 'Αύγ', 'Σεπτ', 'Οκτ', 'Νοέ', 'Δεκ']

    # Αρχικοποίηση λιστών με μηδενικά για τα έσοδα και τα έξοδα κάθε μήνα
    income_data = [0.0] * 12
    expense_data = [0.0] * 12

    try:
        # Λήψη δεδομένων εισόδων και εξόδων ανά μήνα από το αντικείμενο της εφαρμογής
        income_raw = main_app.get_incomes_per_month()   # αναμένεται λίστα από πλειάδες (μήνας, ποσό)
        expense_raw = main_app.get_expenses_per_month()

        # Εισαγωγή των δεδομένων εισόδων στη σωστή θέση της λίστας βάσει του μήνα
        for month_str, value in income_raw:
            index = int(month_str) - 1  # μετατροπή από 1-based σε 0-based
            income_data[index] = value

        # Εισαγωγή των δεδομένων εξόδων στη σωστή θέση της λίστας βάσει του μήνα
        for month_str, value in expense_raw:
            index = int(month_str) - 1
            expense_data[index] = value

    except Exception as e:
        # Εμφάνιση μηνύματος σε περίπτωση αποτυχίας φόρτωσης δεδομένων
        print(f"Σφάλμα φόρτωσης δεδομένων: {e}")

    # Σχεδίαση γραμμής για τα έσοδα (πράσινο χρώμα)
    ax.plot(months_labels, income_data, color='#44f205', linestyle='solid', label='Έσοδα')

    # Σχεδίαση γραμμής για τα έξοδα (κόκκινο χρώμα)
    ax.plot(months_labels, expense_data, color='#f20505', linestyle='solid', label='Έξοδα')

    # Προσθήκη τίτλου διαγράμματος
    ax.set_title("Έσοδα - Έξοδα")

    # Ετικέτα άξονα Υ
    ax.set_ylabel("Ευρώ")

    # Εμφάνιση θρύλου (υπόμνημα γραμμών)
    ax.legend(loc='upper center')

    # Ενσωμάτωση του γραφήματος σε Tkinter μέσω του FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=master)

    # Σχεδίαση του γραφήματος
    canvas.draw()

    # Επιστροφή του widget που μπορεί να προστεθεί σε Tkinter frame
    return canvas.get_tk_widget()

