import sqlite3


class Database:
    def __init__(self):
        self.db_path = "database.db"
        self.con = None
        self.cur = None
        self.initialize_db()

    def initialize_db(self):
        self.con = self.connect()
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
                self.con.execute("PRAGMA foreign_keys = ON;")
            except sqlite3.Error as error:
                print(f"Database error: {error}\nRolling back...")
            finally:
                print("db initialised")
        self.close()

    def connect(self):
        con = sqlite3.connect(self.db_path)
        con.execute("PRAGMA foreign_keys = ON;")
        return con

    def close(self):
        if self.cur:
            self.cur.close()
        if self.con:
            self.con.close()

    def insert_category(self, name):
        self.con = self.connect()
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
                print("category already exist! Rolling back...")
            except sqlite3.Error as error:
                print(f"Database error: {error}\nRolling back...")
        self.close()

    def insert_expense(self, values: tuple):
        self.con = self.connect()
        with self.con:
            try:
                self.con.execute(
                    """
                    INSERT INTO Expense (Name, Value, Category, Monthly, Date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    values,
                )
            except sqlite3.IntegrityError as error:
                print(error)
                print("Rolling back...")
            except sqlite3.Error as error:
                print(f"Database error: {error}\nRolling back...")
        self.close()

    def delete_expense(self, id):
        self.con = self.connect()
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
                print(f"Database error: {error}\nRolling back...")
        self.close()

    def insert_income(self, values: tuple):
        self.con = self.connect()
        with self.con:
            try:
                self.con.execute(
                    """
                    INSERT INTO Income (Name, Value, Category, Monthly, Date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    values,
                )
            except sqlite3.IntegrityError as error:
                print(error)
                print("Rolling back...")
            except sqlite3.Error as error:
                print(f"Database error: {error}\nRolling back...")
        self.close()

    def delete_income(self, id):
        self.con = self.connect()
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
                print(f"Database error: {error}\nRolling back...")
        self.close()

    def get_categories(self):
        categories = []
        self.con = self.connect()
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Category
                    """
                )
                for row in rows:
                    categories.append(row)
            except sqlite3.Error as error:
                print(f"Database error: {error}\nRolling back...")
        self.close()
        return categories

    def get_expenses(self):
        expenses = []
        self.con = self.connect()
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Expense
                    """
                )
                for row in rows:
                    expenses.append(row)
            except sqlite3.Error as error:
                print(f"Database error: {error}\nRolling back...")
        self.close()
        return expenses

    def get_incomes(self):
        incomes = []
        self.con = self.connect()
        with self.con:
            try:
                rows = self.con.execute(
                    """
                    SELECT *
                    FROM Income
                    """
                )
                for row in rows:
                    incomes.append(row)
            except sqlite3.Error as error:
                print(f"Database error: {error}\nRolling back...")
        self.close()
        return incomes


if __name__ == "__main__":
    db = Database()
    db.insert_category(('paok'))
    db.insert_expense(('paok', '20', 1, False, '29-03-1998'))
    db.insert_income(('paok', '20', 1, False, '29-03-1998'))
    print(db.get_expenses())
    print()
    print(db.get_incomes())
