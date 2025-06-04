from sqlite3 import DatabaseError
from database import database
from validator import Validator
from models.income import Income
from models.expense import Expense
import helpers as helpers


class MainError(Exception):
    pass


class Main:
    def __init__(self):
        self.db = database.Database()
        self.categories = self.db.get_categories()
        self.validator = Validator()

    def add_income(self, income: Income):
        self.validator.errors.clear()
        income.date = helpers.format_date(income.date)
        if not self.validator.validate_input(
            self.categories, income.name, income.value, income.category, income.date
        ):
            return helpers.error_response(self.validator.errors)
        values = (
            income.name,
            income.value,
            income.category,
            income.monthly,
            income.date,
        )
        try:
            self.db.insert_income(values)
            return helpers.success_response(None)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def delete_income(self, id):
        self.validator.errors.clear()
        if not self.validator.validate_id(id):
            return helpers.error_response(self.validator.errors)
        try:
            self.db.delete_income(id)
            return helpers.success_response(None)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def edit_income(
        self, id, name=None, value=None, category=None, monthly=None, date=None
    ):
        self.validator.errors.clear()
        updates = []
        params = []
        if name is not None:
            updates.append("Name = (?)")
            params.append(name)
        if value is not None:
            updates.append("Value = (?)")
            params.append(value)
        if category is not None:
            updates.append("Category = (?)")
            params.append(category)
        if date is not None:
            updates.append("Date = (?)")
            params.append(date)
        if monthly is not None:
            updates.append("Monthly = (?)")
            params.append(monthly)
        params.append(id)
        if not updates:
            print("no updates")
            return
        # validate inputs
        try:
            success, message = self.db.edit_income(updates, params)
            if not success:
                print(message)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_income(self):
        try:
            return self.db.get_incomes()
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_expense(self):
        try:
            return self.db.get_expenses()
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def add_expense(self, expense: Expense):
        self.validator.errors.clear()
        expense.date = helpers.format_date(expense.date)
        if not self.validator.validate_input(
            self.categories, expense.name, expense.value, expense.category, expense.date
        ):
            return helpers.error_response(self.validator.errors)
        values = (
            expense.name,
            expense.value,
            expense.category,
            expense.monthly,
            expense.date,
        )
        try:
            self.db.insert_expense(values)
            return helpers.success_response(None)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def delete_expense(self, id):
        self.validator.errors.clear()
        if not self.validator.validate_id(id):
            return helpers.error_response(self.validator.errors)
        try:
            return helpers.success_response(None)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def edit_expense(
        self, id, name=None, value=None, category=None, monthly=None, date=None
    ):
        self.validator.errors.clear()
        updates = []
        params = []
        if name is not None:
            updates.append("Name = (?)")
            params.append(name)
        if value is not None:
            updates.append("Value = (?)")
            params.append(value)
        if category is not None:
            updates.append("Category = (?)")
            params.append(category)
        if date is not None:
            updates.append("Date = (?)")
            params.append(date)
        if monthly is not None:
            updates.append("Monthly = (?)")
            params.append(monthly)
        params.append(id)
        if not updates:
            print("no updates")
            return
        # validate inputs
        try:
            success, message = self.db.edit_expense(updates, params)
            if not success:
                print(message)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def add_category(self, name):
        self.validator.errors.clear()
        if not self.validator.validate_category_input(name):
            return helpers.error_response(self.validator.errors)
        try:
            self.db.insert_category(name)
            self.categories = self.db.get_categories()
            return helpers.success_response(None)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def delete_category(self, id):
        self.validator.errors.clear()
        if not self.validator.validate_id(id):
            return helpers.error_response(self.validator.errors)
        try:
            self.db.delete_category(id)
            self.categories = self.db.get_categories()
            return helpers.success_response(None)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def edit_category(self, id, new_name):
        self.validator.errors.clear()
        if not self.validator.validate_category_input(
            new_name
        ) or not self.validator.validate_id(id):
            return helpers.error_response(self.validator.errors)
        try:
            self.db.edit_category(id, new_name)
            self.categories = self.db.get_categories()
            return helpers.success_response(None)
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_incomes_specific_month(self, month):
        self.validator.errors.clear()
        if not self.validator.validate_value(month):
            print(self.validator.error)
            return helpers.error_response(self.validator.errors)
        try:
            return helpers.success_response(self.db.get_incomes_month(month))
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_expenses_specific_month(self, month):
        self.validator.errors.clear()
        if not self.validator.validate_value(month):
            print(self.validator.error)
            return helpers.error_response(self.validator.errors)
        try:
            return helpers.success_response(self.db.get_expenses_month(month))
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_incomes_per_month(self):
        try:
            return self.db.get_incomes_per_month()
        except DatabaseError as error:
            raise MainError(f"Error: {error}")
            print()
    def get_expenses_per_month(self):
        try:
            return self.db.get_expenses_per_month()
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_incomes_by_category(self, category_id):
        self.validator.errors.clear()
        if not self.validator.validate_category(category_id, self.categories):
            print(self.validator.error)
            return helpers.error_response(self.validator.errors)
        try:
            return helpers.success_response(self.db.get_incomes_per_category(category_id))
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_expenses_by_category(self, category_id):
        self.validator.errors.clear()
        if not self.validator.validate_category(category_id, self.categories):
            print(self.validator.error)
            return helpers.error_response(self.validator.errors)
        try:
            return helpers.success_response(self.db.get_expenses_per_category(category_id))
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_incomes_by_date(self, date):
        self.validator.errors.clear()
        if not self.validator.validate_date(date):
            print(self.validator.errors)
            return helpers.error_response(self.validator.errors)
        date = helpers.format_date(date)
        try:
            return helpers.success_response(self.db.get_incomes_per_date(date))
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_expenses_by_date(self, date):
        self.validator.errors.clear()
        if not self.validator.validate_date(date):
            print(self.validator.errors)
            return helpers.error_response(self.validator.errors)
        date = helpers.format_date(date)
        try:
            return helpers.success_response(self.db.get_expenses_per_date(date))
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_specific_income(self, id):
        self.validator.errors.clear()
        if not self.validator.validate_id(id):
            return helpers.error_response(self.validator.errors)
        try:
            return helpers.success_response(self.db.get_income_by_id(id))
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def get_specific_expense(self, id):
        self.validator.errors.clear()
        if not self.validator.validate_id(id):
            return helpers.error_response(self.validator.errors)
        try:
            return helpers.success_response(self.db.get_expense_by_id(id))
        except DatabaseError as error:
            raise MainError(f"Error: {error}")

    def refresh_chart1(self):
        from monthly_expenses_chart import create_chart1
        if self.chart_widget1:
            self.chart_widget1.destroy()
        self.chart_widget1 = create_chart1(self.chart_frame, self)
        self.chart_widget1.grid(sticky="nsew")


# if __name__ == "__main__":
#     app = Main()
#     # app.add_category("paok")
#     income = Income("paok", "300", 1, False, "3-4-2012")
#     app.add_income(income)
#     # print(app.get_incomes_specific_month(5))
#     # print(app.get_income())
#     # print(app.categories)
#     print(app.get_incomes_by_date("3-4-2012"))
#     # print(app.get_incomes_by_category(1))
#     # print(app.get_incomes_per_month())
