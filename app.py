import tkinter as tk
from tkinter import ttk, messagebox
from guest_manager import GuestManager

class GuestUI:
    def __init__(self, root, db_config):
        self.guest_manager = GuestManager(db_config)
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.tab = ttk.Frame(self.root)
        ttk.Label(self.tab, text="Manage Guests", font=("Arial", 16)).pack(pady=20)

        ttk.Button(self.tab, text="Add Guest", command=self.add_guest).pack(pady=5)
        ttk.Button(self.tab, text="Remove Guest", command=self.remove_guest).pack(pady=5)

        self.tree = ttk.Treeview(self.tab, columns=("GuestID", "FirstName", "LastName", "Phone", "Email", "Address"), show="headings")
        for col in ("GuestID", "FirstName", "LastName", "Phone", "Email", "Address"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.display_guests()

    def add_guest(self):
        # Reuse `add_guest` UI logic here...
        pass

    def remove_guest(self):
        # Reuse `remove_guest` logic...
        pass

    def display_guests(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            guests = self.guest_manager.get_all_guests()
            for guest in guests:
                self.tree.insert("", tk.END, values=(guest["GuestID"], guest["FirstName"], guest["LastName"], guest["Phone"], guest["Email"], guest["Address"]))
        except Exception as e:
            messagebox.showerror("Error", str(e))
