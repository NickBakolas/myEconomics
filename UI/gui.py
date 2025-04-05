import tkinter as tk
from tkinter import messagebox, Menu
from chart1 import create_chart1
from chart2 import create_chart2
from chart3 import create_chart3


def testing():
    messagebox.showinfo("Επιλογή", "Επιλέξατε μια επιλογή από το μενού!")


root = tk.Tk()
root.title("Personal Financial")

root.minsize(800, 400)


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
incomemenu.add_command(label = 'Καταχωρήστε έσοδο', command=testing)
incomemenu.add_command(label = 'Καταχωρήστε έξοδο', command=testing)


frame = tk.Frame(root)
frame.pack(expand=True, fill='both')


frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)


frame1 = tk.Frame(frame)
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

#chart_widget = create_chart1(frame1)
#chart_widget.grid(sticky="nsew")

chart_widget = create_chart3(frame2)
chart_widget.grid(sticky="nsew")

chart_widget = create_chart1(frame3)
chart_widget.grid(sticky="nsew")

chart_widget = create_chart2(frame4)
chart_widget.grid(sticky="nsew")





root.mainloop()
