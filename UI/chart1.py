import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def create_chart1(master):
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    categories = ["Σπίτι", "Αυτοκίνητο", "Ψώνια", "Διασκέδαση", "Λοιπά"]
    num_euros = [800, 300, 400, 150, 100]

    ax.bar(range(len(categories)), num_euros, color='#a832a0')
    ax.set_title("Μηνιαία έξοδα ανα κατηγορία")
    ax.set_ylabel("Euros")
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories)

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    return canvas.get_tk_widget()
