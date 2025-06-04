from datetime import datetime, date as date_type



class Validator:
    def __init__(self):
        self.errors = []

    def validate_input(self, categories, name, value, input_category, date):
        valid = True
        if not self.validate_name(name):
            valid = False
        if not self.validate_value(value):
            valid = False
        if not self.validate_category(input_category, categories):
            valid = False
        if not self.validate_date(date):
            valid = False
        return valid

    def validate_name(self, name):
        if not name:
            self.errors.append("Name cannot be empty")
            return False
        return True

    def validate_value(self, value):
        try:
            value = float(value)
            if value <= 0:
                self.errors.append("Value must be greater than zero")
                return False
            return True
        except ValueError as err:
            self.errors.append(f"Error: {err}")
            return False

    def validate_date(self, value):
        if isinstance(value, date_type):
            return True
        if isinstance(value, str):
            for fmt in ("%d-%m-%Y", "%Y-%m-%d"):
                try:
                    datetime.strptime(value, fmt)
                    return True
                except ValueError:
                    continue
        return False

    def validate_category_input(self, name):
        if not name:
            self.errors.append("name cannot be empty")
            return False
        return True

    def validate_category(self, category, valid_categories):
        valid_categories_ids = [category[0] for category in valid_categories]
        if not self.validate_category_input(category):
            return False
        if category not in valid_categories_ids:
            self.errors.append("Category is not valid")
            return False
        return True

    def validate_id(self, id):
        if not str(id).isdigit():
            self.errors.append("ID must be a digit")
            return False
        if id < 0:
            self.errors.append("id must be >=0")
            return False
        return True
