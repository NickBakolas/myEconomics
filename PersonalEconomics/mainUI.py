import tkinter as tk
from main import Main
from monthly_expenses_chart import create_chart1
from yearly_chart import create_chart2
from monthly_incomes_chart import create_chart3
from PIL import Image, ImageTk
from tkcalendar import Calendar
from expenseUI import open_expense_window
from incomesUI import open_incomes_window
from export_excel import export_data
from datetime import datetime
from daily_chart import daily_bar_chart
from Expenses_managment import open_expenses_details_window
from incomes_managment import  open_income_details_window

main_instance = Main()
main_app = Main()
main_app.chart_frame = None
main_app.chart_widget1 = None

# Συνάρτηση για δημιουργία των εσωτερικών frames
def create_inner_frames(parent):
    frame_left = tk.Frame(parent, width=250)
    frame_left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

    frame_left.grid_rowconfigure(0, weight=1)
    frame_left.grid_rowconfigure(1, weight=1)
    frame_left.grid_columnconfigure(0, weight=1)

    frame_left_top = tk.Frame(frame_left, bg="white")
    frame_left_top.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

    frame_left_bottom = tk.Frame(frame_left, bg="white")
    frame_left_bottom.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    frame_left_bottom.grid_rowconfigure(0, weight=1)
    frame_left_bottom.grid_columnconfigure(0, weight=1)

    frame1 = tk.Frame(parent, bg="white", width=200, height=100)
    frame1.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    frame2 = tk.Frame(parent, bg="white", width=200, height=100)
    frame2.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

    frame3 = tk.Frame(parent, bg="white", width=200, height=100)
    frame3.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    frame4 = tk.Frame(parent, bg="white", width=200, height=100)
    frame4.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

    return frame_left_top, frame_left_bottom, frame1, frame2, frame3, frame4

# Δημιουργία παραθύρου
root = tk.Tk()
root.title("myEconomics")

icon_path = "assets/coin.png"
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

# Κύριο πλαίσιο
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_frame.grid_rowconfigure(0, weight=0)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=0)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

# Δημιουργία εσωτερικών πλαισίων
frame_left_top, frame_left_bottom, frame1, frame2, frame3, frame4 = create_inner_frames(main_frame)
main_app.chart_frame = frame3

# Ημερολόγιο
calendar = Calendar(frame1, date_pattern="dd-mm-yyyy")
calendar.pack(fill=tk.BOTH, expand=True)

def on_date_selected(event=None):
    selected_date_str = calendar.get_date()
    selected_date = datetime.strptime(selected_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

    for widget in frame_left_bottom.winfo_children():
        widget.destroy()

    chart = daily_bar_chart(frame_left_bottom, main_instance, selected_date)
    chart.grid(row=0, column=0, sticky="nsew")

calendar.bind("<<CalendarSelected>>", on_date_selected)
on_date_selected()

# Κουμπιά στο αριστερό πάνω πλαίσιο
tk.Button(frame_left_top, text="Καταχώρηση εσόδων",
          command=lambda: open_incomes_window(main_app)).pack(fill='x', pady=15)
tk.Button(frame_left_top, text="Καταχώρηση δαπανών",
          command=lambda: open_expense_window(main_app)).pack(fill='x', pady=15)
tk.Button(frame_left_top, text="Export data",
          command=lambda: export_data(main_app)).pack(fill='x', pady=15)

# Γραφήματα
main_app.chart_widget1 = create_chart1(frame4, main_app)
main_app.chart_widget1.pack(fill="both", expand=True)

chart_widget2 = create_chart2(frame2, main_app)
chart_widget2.grid(sticky="nsew")

chart_widget3 = create_chart3(frame3, main_app)
chart_widget3.pack(fill="both", expand=True)

# Κουμπιά πάνω δεξιά για αναλυτικά δεδομένα
open_button_incomes = tk.Button(frame3, text="Διαχείριση Εσόδων", command=lambda: open_income_details_window(main_app))
open_button_incomes.place(relx=1.0, y=10, anchor="ne", x=-10)

open_button_expenses = tk.Button(frame4, text="Διαχείριση Εξόδων", command=lambda: open_expenses_details_window(main_app))
open_button_expenses.place(relx=1.0, y=10, anchor="ne", x=-10)

# Ημερήσιο γράφημα
daily_chart_widget = daily_bar_chart(frame_left_bottom, main_instance, datetime.today().strftime('%Y-%m-%d'))
daily_chart_widget.grid(row=0, column=0, sticky="nsew")

# Grid ρυθμίσεις
for frame in [frame1, frame3, frame4]:
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

main_app.chart_frame2 = frame4
main_app.chart_frame3 = frame2
main_app.chart_widget2 = chart_widget2
main_app.chart_widget3 = chart_widget3

root.mainloop()


