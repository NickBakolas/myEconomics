import tkinter as tk
from tkinter import messagebox, simpledialog

def open_category_manager(main_app, refresh_callback=None):
    win = tk.Toplevel()
    win.title("Διαχείριση Κατηγοριών")
    win.geometry("300x400")
    win.configure(bg="white")

    category_listbox = tk.Listbox(win)
    category_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def refresh():
        category_listbox.delete(0, tk.END)
        for cat in main_app.categories:
            category_listbox.insert(tk.END, f"{cat[0]} - {cat[1]}")
        if refresh_callback:
            refresh_callback()

    def add_category():
        name = simpledialog.askstring("Νέα Κατηγορία", "Όνομα:")
        if name:
            main_app.add_category(name)
            refresh()

    def rename_category():
        selected = category_listbox.curselection()
        if not selected:
            return
        cat_id = int(category_listbox.get(selected[0]).split(" - ")[0])
        new_name = simpledialog.askstring("Μετονομασία", "Νέο όνομα:")
        if new_name:
            main_app.edit_category(cat_id, new_name)
            refresh()

    def delete_category():
        selected = category_listbox.curselection()
        if not selected:
            return
        cat_id = int(category_listbox.get(selected[0]).split(" - ")[0])
        if messagebox.askyesno("Επιβεβαίωση", "Διαγραφή κατηγορίας;"):
            main_app.delete_category(cat_id)
            refresh()

    btn_frame = tk.Frame(win, bg="white")
    btn_frame.pack(fill=tk.X, pady=5)

    tk.Button(btn_frame, text="➕ Προσθήκη", command=add_category).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="✏ Μετονομασία", command=rename_category).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="🗑 Διαγραφή", command=delete_category).pack(side=tk.LEFT, padx=5)

    refresh()
