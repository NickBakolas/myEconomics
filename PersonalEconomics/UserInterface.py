import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Menu
from monthly_expenses_chart import create_chart1
from yearly_chart import create_chart2
from monthly_incomes_chart import create_chart3
from PIL import Image, ImageTk


def testing():
    messagebox.showinfo("Επιλογή", "Επιλέξατε μια επιλογή από το μενού!")

def expense():
    clear_frame(frame1)

    label = tk.Label(frame1, text="Καταχωρήστε νέα δαπάνη.", font=("Arial", 16, "bold"), anchor="e", bg="white")
    label.pack(side=tk.TOP, anchor='nw', pady=20)

    # Πρώτο πλαίσιο εισαγωγής
    label_amount = tk.Label(frame1, text="Ποσό:", bg="white")
    label_amount.pack(side=tk.TOP, anchor='nw', padx=20)

    expense_options = ["100", "200", "300", "Άλλο"]
    combo_amount = ttk.Combobox(frame1, values=expense_options)
    combo_amount.pack(side=tk.TOP, anchor='nw', padx=20, pady=5)

    # Δεύτερο πλαίσιο εισαγωγής
    label_category = tk.Label(frame1, text="Κατηγορία:", bg="white")
    label_category.pack(side=tk.TOP, anchor='nw', padx=20)

    category_options = ["Τρόφιμα", "Ενοίκιο", "Λογαριασμοί", "Μεταφορές"]
    combo_category = ttk.Combobox(frame1, values=category_options)
    combo_category.pack(side=tk.TOP, anchor='nw', padx=20, pady=5)

    # Κουμπί για υποβολή επιλογών
    button_submit = tk.Button(frame1, text="Υποβολή",
                              command=lambda: submit_expense(combo_amount.get(), combo_category.get()))
    button_submit.pack(side=tk.TOP, anchor='nw', padx=20, pady=10)


def income():
    clear_frame(frame1)
    label = tk.Label(frame1, text="Καταχωρήστε νέο έσοδο.", font=("Arial", 16, "bold"), anchor="e", bg="white")
    label.pack(side=tk.TOP, anchor='nw', pady=20)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("myEconomics")
root.minsize(1400, 300)

icon_path = "assets/coin.png"
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

menu = Menu(root)
root.config(menu=menu)

monthmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Μήνας', menu=monthmenu)
months = ['Ιανουάριος', 'Φεβρουάριος', 'Μάρτιος', 'Απρίλιος', 'Μάιος',
          'Ιούνιος', 'Ιούλιος', 'Άυγουστος', 'Σεπτέμβριος',
          'Οκτώβριος', 'Νοέμβριος', 'Δεκέμβριος']
for month in months:
    monthmenu.add_command(label=month, command=testing)


yearmenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Έτος', menu=yearmenu)
years = ['2025', '2026']
for year in years:
    yearmenu.add_command(label=year, command=testing)


incomemenu = Menu(menu, tearoff=0)
menu.add_cascade(label ='Καταχώρηση εσόδων-εξόδων',menu=incomemenu)
incomemenu.add_command(label = 'Καταχωρήστε έσοδο', command=income)
incomemenu.add_command(label = 'Καταχωρήστε έξοδο', command=expense)


frame = tk.Frame(root)
frame.pack(expand=True, fill='both')


frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)


frame1 = tk.Frame(frame, bg="white")
frame2 = tk.Frame(frame, bg="green")
frame3 = tk.Frame(frame, bg="blue")
frame4 = tk.Frame(frame, bg="yellow")


frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")
frame3.grid(row=1, column=0, sticky="nsew")
frame4.grid(row=1, column=1, sticky="nsew")

for f in [frame1, frame2, frame3, frame4]:
    f.grid_rowconfigure(0, weight=1)
    f.grid_columnconfigure(0, weight=1)


chart_widget = create_chart3(frame2)
chart_widget.grid(sticky="nsew")

chart_widget = create_chart1(frame3)
chart_widget.grid(sticky="nsew")

chart_widget = create_chart2(frame4)
chart_widget.grid(sticky="nsew")





root.mainloop()