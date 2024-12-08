from database_manager import DatabaseManager

class GuestManager(DatabaseManager):
    def add_guest(self, first_name, last_name, phone, email, address):
        query = "INSERT INTO Guest (FirstName, LastName, Phone, Email, Address) VALUES (%s, %s, %s, %s, %s)"
        self.execute_query(query, (first_name, last_name, phone, email, address))

    def delete_guest(self, guest_id):
        query = "DELETE FROM Guest WHERE GuestID = %s"
        self.execute_query(query, (guest_id,))

    def search_guest(self, conditions, params):
        query = "SELECT * FROM Guest WHERE " + " AND ".join(conditions)
        return self.execute_query(query, params, fetch=True)

    def get_all_guests(self):
        query = "SELECT * FROM Guest"
        return self.execute_query(query, fetch=True)
