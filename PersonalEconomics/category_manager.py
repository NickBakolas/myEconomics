import tkinter as tk
from tkinter import messagebox, simpledialog
import helpers as helpers
from helpers import refresh_all_charts
from PIL import Image, ImageTk

def open_category_manager(main_app, refresh_callback=None):
    # Δημιουργία νέου παραθύρου για τη διαχείριση κατηγοριών
    win = tk.Toplevel()
    win.grab_set()  # Κάνε το παράθυρο modal
    win.title("Διαχείριση Κατηγοριών")
    win.geometry("300x400")
    win.configure(bg="white")

    # Ορισμός εικονιδίου παραθύρου
    icon_path = "assets/coin.png"
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    win.iconphoto(False, icon_photo)

    # Λίστα εμφάνισης των κατηγοριών
    category_listbox = tk.Listbox(win)
    category_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def refresh():
        # Καθαρισμός και επαναφόρτωση των κατηγοριών από την εφαρμογή
        category_listbox.delete(0, tk.END)
        for cat in main_app.categories:
            category_listbox.insert(tk.END, f"{cat[0]} - {cat[1]}")  # cat[0] = id, cat[1] = όνομα
        if refresh_callback:
            refresh_callback()  # Ενημέρωση άλλου τμήματος της εφαρμογής (αν δόθηκε)
        refresh_all_charts(main_app)
    def add_category():
        # Εισαγωγή νέας κατηγορίας μέσω διαλόγου
        name = simpledialog.askstring("Νέα Κατηγορία", "Όνομα:")
        if name:
            main_app.add_category(name)
            refresh()

    def rename_category():
        # Μετονομασία επιλεγμένης κατηγορίας
        selected = category_listbox.curselection()
        if not selected:
            return
        cat_id = int(category_listbox.get(selected[0]).split(" - ")[0])  # Ανάκτηση ID
        new_name = simpledialog.askstring("Μετονομασία", "Νέο όνομα:")
        if new_name:
            main_app.edit_category(cat_id, new_name)
            refresh()

    def delete_category():
        # Διαγραφή επιλεγμένης κατηγορίας
        selected = category_listbox.curselection()
        if not selected:
            return
        cat_id = int(category_listbox.get(selected[0]).split(" - ")[0])  # Ανάκτηση ID
        if messagebox.askyesno("Επιβεβαίωση", "Διαγραφή κατηγορίας;"):
            main_app.delete_category(cat_id)
            refresh()

    # Πλαίσιο για τα κουμπιά
    btn_frame = tk.Frame(win, bg="white")
    btn_frame.pack(fill=tk.X, pady=5)

    # Κουμπιά για προσθήκη, μετονομασία, διαγραφή κατηγορίας
    tk.Button(btn_frame, text="➕ Προσθήκη", command=add_category).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="✏ Μετονομασία", command=rename_category).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="🗑 Διαγραφή", command=delete_category).pack(side=tk.LEFT, padx=5)

    # Αρχική φόρτωση κατηγοριών
    refresh()

