from datetime import datetime, date


def date_comparison_with_today(date_):
    date_obj = datetime.strptime(date_, "%d-%m-%Y").date()
    today = date.today()
    if date_obj > today:
        return False
    else:
        return True


def add_month_to_date(date_):
    date_obj = datetime.strptime(date_, "%d-%m-%Y")
    if date_obj.month == 12:
        return datetime.strftime(
            date_obj.replace(year=date_obj.year + 1, month=1), "%d-%m-%Y"
        )
    else:
        return datetime.strftime(date_obj.replace(month=date_obj.month + 1), "%d-%m-%Y")


def get_monthly_incomes(con):
    incomes_to_update = []
    monthly_incomes = con.execute("""
                        SELECT *
                        FROM income
                        WHERE Monthly = 1 AND
                                (SUBSTR(income.date, 7, 4) || '-' || SUBSTR(income.date, 4, 2) || '-' || SUBSTR(income.date, 1, 2)) <= DATE('now')
                        AND (SUBSTR(income.date, 7, 4) || '-' || SUBSTR(income.date, 4, 2)) != SUBSTR(DATE('now'), 1, 7);
                    """)
    for income in monthly_incomes.fetchall():
        if date_comparison_with_today(income[5]):
            incomes_to_update.append(income)
    return incomes_to_update


def get_monthly_expenses(con):
    expenses_to_update = []
    monthly_expenses = con.execute("""
                        SELECT *
                        FROM income
                        WHERE Monthly = 1 AND
                                (SUBSTR(income.date, 7, 4) || '-' || SUBSTR(income.date, 4, 2) || '-' || SUBSTR(income.date, 1, 2)) <= DATE('now')
                        AND (SUBSTR(income.date, 7, 4) || '-' || SUBSTR(income.date, 4, 2)) != SUBSTR(DATE('now'), 1, 7);
                    """)
    for expense in monthly_expenses.fetchall():
        if date_comparison_with_today(expense[5]):
            expenses_to_update.append(expense)
    return expenses_to_update
