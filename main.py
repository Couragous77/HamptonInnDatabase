import tkinter as tk
from tkinter import ttk
from app import GuestUI

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'HamptonInnDB'
}

root = tk.Tk()
root.title("Hampton Inn Management System")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

guest_ui = GuestUI(notebook, db_config)
notebook.add(guest_ui.tab, text="Guests")

root.mainloop()
