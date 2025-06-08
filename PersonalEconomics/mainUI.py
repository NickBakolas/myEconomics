import tkinter as tk  # GUI toolkit
from main import Main  # Κεντρική λογική εφαρμογής
from expenses_chart import create_chart1  # Γράφημα εξόδων ανά κατηγορία
from month_chart import create_chart2  # Γράφημα μηνιαίων εξόδων
from incomes_chart import create_chart3  # Γράφημα εσόδων
from PIL import Image, ImageTk  # Για εισαγωγή εικόνας εικονιδίου
from tkcalendar import Calendar  # Ημερολόγιο επιλογής ημερομηνίας
from expenseUI import open_expense_window  # Παράθυρο καταχώρησης εξόδων
from incomesUI import open_incomes_window  # Παράθυρο καταχώρησης εσόδων
from export_excel import export_data  # Εξαγωγή δεδομένων σε Excel
from datetime import datetime  # Για μετατροπή/διαχείριση ημερομηνιών
from daily_chart import daily_bar_chart  # Ημερήσιο γράφημα
from Expenses_managment import open_expenses_details_window  # Παράθυρο διαχείρισης εξόδων
from incomes_managment import open_incomes_details_window  # Παράθυρο διαχείρισης εσόδων

# Δημιουργία instance της βασικής κλάσης εφαρμογής
main_app = Main()

# Συνάρτηση δημιουργίας εσωτερικών frames για layout
def create_inner_frames(parent):
    # Αριστερό πλαίσιο που περιέχει τα top/bottom υπο-frames
    frame_left = tk.Frame(parent, width=250)
    frame_left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
    frame_left.grid_rowconfigure(0, weight=1)
    frame_left.grid_rowconfigure(1, weight=1)
    frame_left.grid_columnconfigure(0, weight=1)

    # Πάνω μέρος του αριστερού πλαισίου (κουμπιά)
    frame_left_top = tk.Frame(frame_left, bg="white")
    frame_left_top.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
    frame_left_top.grid_rowconfigure(0, weight=1)
    frame_left_top.grid_columnconfigure(0, weight=1)

    # Κάτω μέρος του αριστερού πλαισίου (γράφημα ημερήσιο)
    frame_left_bottom = tk.Frame(frame_left, bg="white")
    frame_left_bottom.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    frame_left_bottom.grid_rowconfigure(0, weight=1)
    frame_left_bottom.grid_columnconfigure(0, weight=1)

    # Frame με το ημερολόγιο
    frame1 = tk.Frame(parent, bg="white", width=200, height=100)
    frame1.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    frame1.grid_rowconfigure(0, weight=1)
    frame1.grid_columnconfigure(0, weight=1)

    # Frame με γράφημα μηνιαίων εξόδων
    frame2 = tk.Frame(parent, bg="white", width=200, height=100)
    frame2.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)

    # Frame με γράφημα εσόδων
    frame3 = tk.Frame(parent, bg="white", width=200, height=100)
    frame3.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    frame3.grid_rowconfigure(0, weight=1)
    frame3.grid_columnconfigure(0, weight=1)

    # Frame με γράφημα εξόδων ανά κατηγορία
    frame4 = tk.Frame(parent, bg="white", width=200, height=100)
    frame4.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
    frame4.grid_rowconfigure(0, weight=1)
    frame4.grid_columnconfigure(0, weight=1)

    return frame_left_top, frame_left_bottom, frame1, frame2, frame3, frame4

# Ρύθμιση κύριου παραθύρου
root = tk.Tk()
root.title("myEconomics")

# Ορισμός αρχικού μεγέθους και κεντράρισμα
window_width = 1300
window_height = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Ορισμός εικονιδίου παραθύρου
icon_path = "assets/coin.png"
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

# Κύριο frame περιεχομένου
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew")

# Κάνει το κύριο παράθυρο responsive
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Κάνει το κύριο frame responsive σε 2 γραμμές και 3 στήλες
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

# Δημιουργία και τοποθέτηση των εσωτερικών frames
frame_left_top, frame_left_bottom, frame1, frame2, frame3, frame4 = create_inner_frames(main_frame)
main_app.chart_frame = frame3  # Χρήσιμο για επαναφόρτωση γραφήματος από αλλού

# Προσθήκη ημερολογίου
calendar = Calendar(frame1, date_pattern="dd-mm-yyyy")
calendar.grid(row=0, column=0, sticky="nsew")

# Callback όταν επιλεγεί ημερομηνία από το ημερολόγιο
def on_date_selected(event=None):
    selected_date_str = calendar.get_date()
    selected_date = datetime.strptime(selected_date_str, "%d-%m-%Y").strftime("%Y-%m-%d")
    # Καθαρισμός προηγούμενου γραφήματος
    for widget in frame_left_bottom.winfo_children():
        widget.destroy()
    # Δημιουργία νέου γραφήματος για την επιλεγμένη ημέρα
    chart = daily_bar_chart(frame_left_bottom, main_app, selected_date)
    chart.grid(row=0, column=0, sticky="nsew")

# Σύνδεση callback στην επιλογή ημερομηνίας
calendar.bind("<<CalendarSelected>>", on_date_selected)
# Αρχική εμφάνιση γραφήματος για τη σημερινή ημέρα
on_date_selected()

# Κουμπιά για βασικές λειτουργίες (εισαγωγή, διαχείριση, εξαγωγή)
tk.Button(frame_left_top, text="Καταχώρηση εσόδων",
          command=lambda: open_incomes_window(main_app)).pack(fill='y', pady=15)

tk.Button(frame_left_top, text="Καταχώρηση δαπανών",
          command=lambda: open_expense_window(main_app)).pack(fill='y', pady=15)

tk.Button(frame_left_top, text="Διαχείριση Εσόδων",
          command=lambda: open_incomes_details_window(main_app)).pack(fill='y', pady=15)

tk.Button(frame_left_top, text="Διαχείριση Δαπανών",
          command=lambda: open_expenses_details_window(main_app)).pack(fill='y', pady=15)

tk.Button(frame_left_top, text="Export data",
          command=lambda: export_data(main_app)).pack(fill='y', pady=15)

# Δημιουργία και τοποθέτηση γραφημάτων στα αντίστοιχα frames
chart_widget3 = create_chart3(frame3, main_app)
chart_widget3.grid(row=0, column=0, sticky="nsew")

main_app.chart_widget1 = create_chart1(frame4, main_app)
main_app.chart_widget1.grid(row=0, column=0, sticky="nsew")

chart_widget2 = create_chart2(frame2, main_app)
chart_widget2.grid(row=0, column=0, sticky="nsew")

daily_chart_widget = daily_bar_chart(frame_left_bottom, main_app, datetime.today().strftime('%Y-%m-%d'))
daily_chart_widget.grid(row=0, column=0, sticky="nsew")

# Αντιστοίχιση frames στα attributes για πιθανή χρήση από άλλα modules
main_app.chart_frame1 = frame4
main_app.chart_frame2 = frame2
main_app.chart_frame3 = frame3

# Αντιστοίχιση ημερολογίου, frame και chart στο main_app για ανανέωση από αλλού
main_app.calendar = calendar
main_app.daily_chart_frame = frame_left_bottom
main_app.daily_chart_widget = daily_chart_widget


# Εκκίνηση του GUI loop
root.mainloop()





