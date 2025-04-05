import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_chart3(master):
    # Δεδομένα
    categories = ["Σπίτι", "Αυτοκίνητο", "Ψώνια", "Διασκέδαση", "Λοιπά"]
    num_euros = [800, 300, 400, 150, 100]

    colors = ['#a832a0', '#32a0a8', '#a8a832', '#a83232', '#32a832']

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    ax.pie(num_euros, labels=categories, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True)

    ax.axis('equal')
    plt.title("Μηνιαία Έξοδα ανά Κατηγορία")

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    return canvas.get_tk_widget()
