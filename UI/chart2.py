import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_chart2(master):
    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)

    months = ['Ιαν', 'Φεβρ', 'Μάρτ', 'Απρ', 'Μαι', 'Ιού', 'Ιούλ', 'Αύγ', 'Σεπτ', 'Οκτ', 'Νοέμβρ','Δεκ']
    income = [1200, 1250, 1220, 1300, 1100, 1300, 1200, 1330, 1100, 1180, 1300, 2200]
    outcome = [1000, 800, 900, 600, 400, 800, 500, 660, 250, 650, 800, 1100]

    plt.plot(months, income, color='#44f205', marker='', linestyle='solid',label= 'Έσοδα')
    plt.plot(months, outcome, color='#f20505', marker='', linestyle='solid', label= 'Έξοδα')


    plt.title("Έσοδα-Έξοδα")
    plt.ylabel("Ευρώ")
    plt.legend(loc=9)

    canvas = FigureCanvasTkAgg(fig, master=master)
    canvas.draw()
    return canvas.get_tk_widget()