from datetime import datetime, date as date_type

# Κλάση υπεύθυνη για την επικύρωση δεδομένων εισόδου
class Validator:
    def __init__(self):
        self.errors = []  # Λίστα για αποθήκευση μηνυμάτων σφάλματος

    # Κύρια συνάρτηση επικύρωσης όλων των πεδίων
    def validate_input(self, categories, name, value, input_category, date):
        valid = True
        if not self.validate_name(name):  # Έλεγχος περιγραφής
            valid = False
        if not self.validate_value(value):  # Έλεγχος ποσού
            valid = False
        if not self.validate_category(input_category, categories):  # Έλεγχος κατηγορίας
            valid = False
        if not self.validate_date(date):  # Έλεγχος ημερομηνίας
            valid = False
        return valid

    # Επικύρωση ονόματος/περιγραφής
    def validate_name(self, name):
        if not name:
            self.errors.append("Name cannot be empty")
            return False
        return True

    # Επικύρωση ποσού
    def validate_value(self, value):
        try:
            value = float(value)
            if value <= 0:
                self.errors.append("Value must be greater than zero")
                return False
            return True
        except ValueError as err:
            self.errors.append(f"Error: {err}")  # Σφάλμα μετατροπής σε float
            return False

    # Επικύρωση ημερομηνίας (είτε date είτε str σε έγκυρη μορφή)
    def validate_date(self, value):
        if isinstance(value, date_type):  # Αν είναι ήδη αντικείμενο date
            return True
        if isinstance(value, str):  # Αν είναι string, δοκίμασε να το μετατρέψεις
            for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
                try:
                    datetime.strptime(value, fmt)
                    return True
                except ValueError:
                    continue
        return False  # Αν καμία μορφή δεν ταιριάζει

    # Έλεγχος αν το όνομα της κατηγορίας είναι έγκυρο (μη κενό)
    def validate_category_input(self, name):
        if not name:
            self.errors.append("name cannot be empty")
            return False
        return True

    # Επικύρωση κατηγορίας από λίστα έγκυρων κατηγοριών
    def validate_category(self, category, valid_categories):
        valid_categories_ids = [category[0] for category in valid_categories]  # Λίστα έγκυρων IDs
        if not self.validate_category_input(category):  # Έλεγχος αν είναι μη κενή
            return False
        if category not in valid_categories_ids:  # Έλεγχος αν υπάρχει στα έγκυρα IDs
            self.errors.append("Category is not valid")
            return False
        return True

    # Επικύρωση ID (πρέπει να είναι αριθμός και >=0)
    def validate_id(self, id):
        if not str(id).isdigit():  # Έλεγχος αν είναι ψηφίο
            self.errors.append("ID must be a digit")
            return False
        if id < 0:  # Μη αρνητικό
            self.errors.append("id must be >=0")
            return False
        return True

