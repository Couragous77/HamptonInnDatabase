import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database connection configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'HamptonInnDB'
}

# Helper Functions
def execute_query(query, params=None, fetch=False, fetchall=True):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True if fetch else False)
        cursor.execute(query, params or [])
        if fetch:
            return cursor.fetchall() if fetchall else cursor.fetchone()
        conn.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Add Guest
def add_guest():
    def submit():
        query = "INSERT INTO Guest (FirstName, LastName, Phone, Email, Address) VALUES (%s, %s, %s, %s, %s)"
        params = (first_name_entry.get(), last_name_entry.get(), phone_entry.get(), email_entry.get(), address_entry.get())
        execute_query(query, params)
        messagebox.showinfo("Success", "Guest added successfully!")
        add_guest_window.destroy()
        show_all_guests()

    add_guest_window = tk.Toplevel(root)
    add_guest_window.title("Add Guest")

    ttk.Label(add_guest_window, text="First Name").grid(row=0, column=0, padx=10, pady=5)
    first_name_entry = ttk.Entry(add_guest_window)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(add_guest_window, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
    last_name_entry = ttk.Entry(add_guest_window)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(add_guest_window, text="Phone").grid(row=2, column=0, padx=10, pady=5)
    phone_entry = ttk.Entry(add_guest_window)
    phone_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(add_guest_window, text="Email").grid(row=3, column=0, padx=10, pady=5)
    email_entry = ttk.Entry(add_guest_window)
    email_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(add_guest_window, text="Address").grid(row=4, column=0, padx=10, pady=5)
    address_entry = ttk.Entry(add_guest_window)
    address_entry.grid(row=4, column=1, padx=10, pady=5)

    ttk.Button(add_guest_window, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=10)

# Remove Guest
def remove_guest():
    selected = guest_tree.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a guest to remove.")
        return
    guest_id = guest_tree.item(selected, "values")[0]
    query = "DELETE FROM Guest WHERE GuestID = %s"
    execute_query(query, (guest_id,))
    messagebox.showinfo("Success", "Guest removed successfully!")
    show_all_guests()

# Search Guest
def search_guest():
    def perform_search():
        query = "SELECT * FROM Guest WHERE FirstName LIKE %s OR LastName LIKE %s OR Phone LIKE %s OR Email LIKE %s"
        param = f"%{search_entry.get()}%"
        results = execute_query(query, (param, param, param, param), fetch=True)
        for row in guest_tree.get_children():
            guest_tree.delete(row)
        for guest in results:
            guest_tree.insert("", tk.END, values=(guest["GuestID"], guest["FirstName"], guest["LastName"], guest["Phone"], guest["Email"], guest["Address"]))

    search_window = tk.Toplevel(root)
    search_window.title("Search Guest")

    ttk.Label(search_window, text="Enter search term").pack(pady=5)
    search_entry = ttk.Entry(search_window)
    search_entry.pack(pady=5)
    ttk.Button(search_window, text="Search", command=perform_search).pack(pady=10)

# Show All Guests
def show_all_guests():
    for row in guest_tree.get_children():
        guest_tree.delete(row)
    query = "SELECT * FROM Guest"
    guests = execute_query(query, fetch=True)
    for guest in guests:
        guest_tree.insert("", tk.END, values=(guest["GuestID"], guest["FirstName"], guest["LastName"], guest["Phone"], guest["Email"], guest["Address"]))

def add_room():
    def submit():
        query = "INSERT INTO Room (RoomNumber, RoomType, Price, Availability) VALUES (%s, %s, %s, %s)"
        params = (room_number_entry.get(), room_type_combobox.get(), price_entry.get(), availability_combobox.get())
        execute_query(query, params)
        messagebox.showinfo("Success", "Room added successfully!")
        add_room_window.destroy()
        show_all_rooms()

    add_room_window = tk.Toplevel(root)
    add_room_window.title("Add Room")

    ttk.Label(add_room_window, text="Room Number").grid(row=0, column=0, padx=10, pady=5)
    room_number_entry = ttk.Entry(add_room_window)
    room_number_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(add_room_window, text="Room Type").grid(row=1, column=0, padx=10, pady=5)
    room_type_combobox = ttk.Combobox(add_room_window, values=["Single", "Double", "Suite"])
    room_type_combobox.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(add_room_window, text="Price").grid(row=2, column=0, padx=10, pady=5)
    price_entry = ttk.Entry(add_room_window)
    price_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(add_room_window, text="Availability").grid(row=3, column=0, padx=10, pady=5)
    availability_combobox = ttk.Combobox(add_room_window, values=["Available", "Unavailable"])
    availability_combobox.grid(row=3, column=1, padx=10, pady=5)

    ttk.Button(add_room_window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

def show_all_rooms():
    for row in room_tree.get_children():
        room_tree.delete(row)
    query = "SELECT * FROM Room"
    rooms = execute_query(query, fetch=True)
    for room in rooms:
        room_tree.insert("", tk.END, values=(room["RoomID"], room["RoomNumber"], room["RoomType"], room["Price"], room["Availability"]))

# Booking Management
def add_booking():
    def submit():
        query = """
            INSERT INTO Booking (GuestID, RoomID, CheckInDate, CheckOutDate)
            VALUES (%s, %s, %s, %s)
        """
        params = (guest_id_entry.get(), room_id_entry.get(), check_in_date_entry.get(), check_out_date_entry.get())
        execute_query(query, params)
        messagebox.showinfo("Success", "Booking added successfully!")
        add_booking_window.destroy()
        show_all_bookings()

    add_booking_window = tk.Toplevel(root)
    add_booking_window.title("Add Booking")

    ttk.Label(add_booking_window, text="Guest ID").grid(row=0, column=0, padx=10, pady=5)
    guest_id_entry = ttk.Entry(add_booking_window)
    guest_id_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(add_booking_window, text="Room ID").grid(row=1, column=0, padx=10, pady=5)
    room_id_entry = ttk.Entry(add_booking_window)
    room_id_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(add_booking_window, text="Check-In Date (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5)
    check_in_date_entry = ttk.Entry(add_booking_window)
    check_in_date_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(add_booking_window, text="Check-Out Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5)
    check_out_date_entry = ttk.Entry(add_booking_window)
    check_out_date_entry.grid(row=3, column=1, padx=10, pady=5)

    ttk.Button(add_booking_window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

def show_all_bookings():
    for row in booking_tree.get_children():
        booking_tree.delete(row)
    query = "SELECT * FROM Booking"
    bookings = execute_query(query, fetch=True)
    for booking in bookings:
        booking_tree.insert("", tk.END, values=(booking["BookingID"], booking["GuestID"], booking["RoomID"], booking["CheckInDate"], booking["CheckOutDate"]))

# Payment Management
def add_payment():
    def submit():
        query = "INSERT INTO Payment (BookingID, Amount, PaymentDate) VALUES (%s, %s, %s)"
        params = (booking_id_entry.get(), amount_entry.get(), payment_date_entry.get())
        execute_query(query, params)
        messagebox.showinfo("Success", "Payment added successfully!")
        add_payment_window.destroy()
        show_all_payments()

    add_payment_window = tk.Toplevel(root)
    add_payment_window.title("Add Payment")

    ttk.Label(add_payment_window, text="Booking ID").grid(row=0, column=0, padx=10, pady=5)
    booking_id_entry = ttk.Entry(add_payment_window)
    booking_id_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(add_payment_window, text="Amount").grid(row=1, column=0, padx=10, pady=5)
    amount_entry = ttk.Entry(add_payment_window)
    amount_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(add_payment_window, text="Payment Date (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5)
    payment_date_entry = ttk.Entry(add_payment_window)
    payment_date_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Button(add_payment_window, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=10)

def show_all_payments():
    for row in payment_tree.get_children():
        payment_tree.delete(row)
    query = "SELECT * FROM Payment"
    payments = execute_query(query, fetch=True)
    for payment in payments:
        payment_tree.insert("", tk.END, values=(payment["PaymentID"], payment["BookingID"], payment["Amount"], payment["PaymentDate"]))

# UI Setup
root = tk.Tk()
root.title("Hampton Inn Management System")
root.geometry("1200x800")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

tabs = {
    "Dashboard": ttk.Frame(notebook),
    "Guests": ttk.Frame(notebook),
    "Rooms": ttk.Frame(notebook),
    "Bookings": ttk.Frame(notebook),
    "Payments": ttk.Frame(notebook),
    "Reports": ttk.Frame(notebook),
    "Services": ttk.Frame(notebook)
}

for tab_name, tab_frame in tabs.items():
    notebook.add(tab_frame, text=tab_name)

# Guests Tab
ttk.Label(tabs["Guests"], text="Manage Guests", font=("Arial", 16)).pack(pady=10)
ttk.Button(tabs["Guests"], text="Add Guest", command=add_guest).pack(pady=5)
ttk.Button(tabs["Guests"], text="Remove Guest", command=remove_guest).pack(pady=5)
ttk.Button(tabs["Guests"], text="Search Guest", command=search_guest).pack(pady=5)
ttk.Button(tabs["Guests"], text="Show All Guests", command=show_all_guests).pack(pady=5)

guest_tree = ttk.Treeview(tabs["Guests"], columns=("GuestID", "FirstName", "LastName", "Phone", "Email", "Address"), show="headings")
guest_tree.heading("GuestID", text="Guest ID")
guest_tree.heading("FirstName", text="First Name")
guest_tree.heading("LastName", text="Last Name")
guest_tree.heading("Phone", text="Phone")
guest_tree.heading("Email", text="Email")
guest_tree.heading("Address", text="Address")
guest_tree.pack(fill=tk.BOTH, expand=True)

show_all_guests()  # Load guests at startup

# Implement Room, Booking, Payment, Reports, and Services similarly

root.mainloop()
