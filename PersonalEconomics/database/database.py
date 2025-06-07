import sqlite3
import os
from .database_helpers import (
    add_month_to_date,
    get_monthly_expenses,
    get_monthly_incomes,
)
from datetime import datetime


class DatabaseError(Exception):
    """
    Κλάση βοηθός που έχει γονέα την κλάση Exception και θα χρησιμοποιηθεί για να δηλώνει σφάλματα που προέρχονται απο την β.δ.
    """

    pass


class Database:
    def __init__(self):
        fileDir = os.path.dirname(__file__)
        self.db_path = os.path.join(fileDir, "database.db")
        self.con = self.connect()
        self.initialize_db()
        self.check_monthly_transactions()

    def __del__(self):
        self.close()

    def initialize_db(self):
        with self.con:
            try:
                self.con.executescript(
                    """
                CREATE TABLE IF NOT EXISTS Category (
                    id INTEGER PRIMARY KEY,
                    Name TEXT UNIQUE
                );

                CREATE TABLE IF NOT EXISTS Expense (
                    id INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Value REAL NOT NULL,
                    Category INTEGER,
                    Monthly INTEGER NOT NULL DEFAULT 0,
                    Date TEXT NOT NULL,
                    FOREIGN  KEY (Category) REFERENCES Category(id)
                );

                CREATE TABLE IF NOT EXISTS Income (
                    id INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    Value REAL NOT NULL,
                    Category INTEGER,
                    Monthly INTEGER NOT NULL DEFAULT 0,
                    Date TEXT NOT NULL,
                    FOREIGN  KEY (Category) REFERENCES Category(id)
                )
                """
                )
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def check_monthly_transactions(self):
        with self.con:
            try:
                # Incomes to update
                incomes_to_update = get_monthly_incomes(self.con)
                expenses_to_update = get_monthly_expenses(self.con)
                query = """
                        UPDATE Income
                        SET monthly = 0
                        WHERE id = ?
                        """
                self.con.executemany(query, [(id[0],)
                                     for id in incomes_to_update])
                query = """
                        UPDATE Expense
                        SET monthly = 0
                        WHERE id = ?
                        """
                self.con.executemany(query, [(id[0],)
                                     for id in expenses_to_update])
                # Insert new incomes/expenses
                # Manipulate income's date
                new_incomes = []
                new_expenses = []
                for income in incomes_to_update:
                    new_income = [x for x in income[:-1]]
                    new_income.append(add_month_to_date(income[5]))
                    new_incomes.append(tuple(new_income))

                for expense in expenses_to_update:
                    new_expense = [x for x in expense[:-1]]
                    new_expense.append(add_month_to_date(expense[5]))
                    new_expenses.append(tuple(new_expense))
                query = """
                        INSERT INTO Income
                        (Name,Value,Category,Monthly ,Date)
                        VALUES (?, ?, ?, ?, ?)
                        """
                if incomes_to_update:
                    self.con.executemany(
                        query, [income[1:] for income in new_incomes])
                query = """
                        INSERT INTO Expense
                        (Name,Value,Category,Monthly ,Date)
                        VALUES (?, ?, ?, ?, ?)
                        """
                if expenses_to_update:
                    self.con.executemany(
                        query, [expense[1:] for expense in new_expenses]
                    )
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def connect(self):
        con = sqlite3.connect(self.db_path)
        con.execute("PRAGMA foreign_keys = ON;")
        return con

    def close(self):
        if self.con:
            self.con.close()

    def insert_category(self, name):
        with self.con:
            try:
                self.con.execute(
                    """
                INSERT INTO Category (Name)
                VALUES (?)
                    """,
                    (name,),
                )
            except sqlite3.IntegrityError:
                raise DatabaseError("Category already exists.")
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def edit_category(self, id, new_name):
        response = ()
        with self.con:
            try:
                result = self.con.execute(
                    "SELECT 1 FROM Category WHERE id = (?)", (id,)
                )
                if not result.fetchone():
                    response = (False, f"No record found with ID {id}")
                    return response

                self.con.execute(
                    """
                UPDATE Category
                SET Name = (?)
                WHERE id = (?)
                    """,
                    (new_name, id),
                )
                response = (True, "updated successfully")
                return response
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def delete_category(self, id):
        with self.con:
            try:
                self.con.execute(
                    """
                DELETE FROM Category
                WHERE id = (?)
                    """,
                    (id,),
                )
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def insert_expense(self, values: tuple):
        with self.con:
            try:
                self.con.execute(
                    """
                    INSERT INTO Expense (Name, Value, Category, Monthly, Date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    values,
                )
            except sqlite3.IntegrityError:
                raise DatabaseError("Expense already exists.")
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def delete_expense(self, id):
        with self.con:
            try:
                self.con.execute(
                    """
                    DELETE FROM Expense
                    WHERE id = ?
                    """,
                    (id,),
                )
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def edit_expense(self, updates, params):
        response = ()
        with self.con:
            try:
                result = self.con.execute(
                    "SELECT 1 FROM Expense WHERE id = (?)", (params[-1],)
                )
                if not result.fetchone():
                    response = (False, f"No record found with ID {params[-1]}")
                    return response
                self.con.execute(
                    f"""
                    UPDATE Expense
                    SET {", ".join(updates)} 
                    WHERE id = (?)
                    """,
                    params,
                )
                response = (True, "Update record")
                return response
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def insert_income(self, values: tuple):
        with self.con:
            try:
                self.con.execute(
                    """
                    INSERT INTO Income (Name, Value, Category, Monthly, Date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    values,
                )
            except sqlite3.IntegrityError:
                raise DatabaseError("Income already exists.")
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def delete_income(self, id):
        with self.con:
            try:
                self.con.execute(
                    """
                    DELETE FROM Income
                    WHERE id = ?
                    """,
                    (id,),
                )
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def edit_income(self, updates, params):
        response = ()
        with self.con:
            try:
                result = self.con.execute(
                    "SELECT 1 FROM Income WHERE id = (?)", (params[-1],)
                )
                if not result.fetchone():
                    response = (False, f"No record found with ID {params[-1]}")
                    return response
                self.con.execute(
                    f"""
                    UPDATE Income
                    SET {", ".join(updates)} 
                    WHERE id = (?)
                    """,
                    params,
                )
                response = (True, "Update record")
                return response
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")

    def get_categories(self):
        categories = []
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Category
                    """
                )
                for row in rows.fetchall():
                    categories.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return categories

    def get_expenses(self):
        expenses = []
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Expense
                    """
                )
                for row in rows.fetchall():
                    expenses.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return expenses

    def get_incomes(self):
        incomes = []
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Income
                    """
                )
                for row in rows.fetchall():
                    incomes.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return incomes

    def get_incomes_month(self, month):
        year = datetime.now().year
        incomes = []
        with self.con:
            try:
                rows = self.con.execute(f"""
                    SELECT *
                    FROM Income
                    WHERE Date LIKE '%-{month:02d}-{year}'
                """)
                for row in rows.fetchall():
                    incomes.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return incomes

    def get_expenses_month(self, month):
        year = datetime.now().year
        expenses = []
        with self.con:
            try:
                rows = self.con.execute(f"""
                    SELECT *
                    FROM Expense
                    WHERE Date LIKE '%-{month:02d}-{year}'
                """)
                for row in rows.fetchall():
                    expenses.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return expenses

    def get_incomes_per_month(self):
        incomes = []
        with self.con:
            try:
                rows = self.con.execute("""
                    SELECT substr(Date, 4, 2) AS month, SUM(Value)
                    FROM Income
                    GROUP BY month
                """)
                for row in rows.fetchall():
                    incomes.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return incomes

    def get_expenses_per_month(self):
        expenses = []
        with self.con:
            try:
                rows = self.con.execute("""
                    SELECT substr(Date, 4, 2) AS month, SUM(Value)
                    FROM Expense
                    GROUP BY month
                """)
                for row in rows.fetchall():
                    expenses.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return expenses

    def get_incomes_per_category(self, category_id):
        incomes = []
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Income
                    WHERE Category = (?);
                """,
                    (category_id,),
                )
                for row in rows.fetchall():
                    incomes.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return incomes

    def get_expenses_per_category(self, category_id):
        expenses = []
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Expense
                    WHERE Category = (?);
                """,
                    (category_id,),
                )
                for row in rows.fetchall():
                    expenses.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return expenses

    def get_incomes_per_date(self, date):
        incomes = []
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Income
                    WHERE Date = (?);
                """,
                    (date,),
                )
                for row in rows.fetchall():
                    incomes.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return incomes

    def get_expenses_per_date(self, date):
        expenses = []
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Expense
                    WHERE Date = (?);
                """,
                    (date,),
                )
                for row in rows.fetchall():
                    expenses.append(row)
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return expenses

    def get_expense_by_id(self, id):
        expense = None
        with self.con:
            try:
                result = self.con.execute(
                    """
                    SELECT *
                    FROM Expense
                    WHERE id = (?);
                """,
                    (id,),
                )
                expense = result.fetchone()
                if not expense:
                    raise DatabaseError(f"No record found with ID {id}")
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return expense

    def get_income_by_id(self, id):
        income = None
        with self.con:
            try:
                result = self.con.execute(
                    """
                    SELECT *
                    FROM Income
                    WHERE id = (?);
                """,
                    (id,),
                )
                income = result.fetchone()
                if not income:
                    raise DatabaseError(f"No record found with ID {id}")
            except sqlite3.Error as error:
                raise DatabaseError(f"Database Error: {error}")
        return income



if __name__ == "__main__":
    db = Database()
    db.insert_category(("frouta"))
    db.insert_expense(("paok", "20", 1, False, "29-03-1998"))
    db.insert_income(("paok", "20", 1, False, "29-03-1998"))
    print(db.get_expenses())
    print()
    print(db.get_incomes())
