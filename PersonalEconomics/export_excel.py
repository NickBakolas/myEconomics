from tkinter import messagebox
from main import MainError
import xlsxwriter

# Συνάρτηση για εξαγωγή δεδομένων σε αρχείο Excel για συγκεκριμένο μήνα
def export_data(app, month):
    try:
        # Βεβαιώσου ότι ο μήνας είναι ακέραιος
        month = int(month)
        print(month)

        # Όνομα του αρχείου εξαγωγής
        filename = f"transactions_{month}.xlsx"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet("Transactions")

        # Δημιουργία μορφοποιήσεων για headers, ημερομηνία, νομισματικά ποσά
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
            'font_color': 'white',
            'border': 1
        })
        date_format = workbook.add_format({'num_format': 'dd-mm-yyyy'})
        currency_format = workbook.add_format({'num_format': '#,##0.00'})

        # Ειδικές μορφοποιήσεις για sections και σύνολα
        expense_header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#FFC7CE',
            'font_color': '#9C0006',
            'border': 1
        })
        income_header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#C6EFCE',
            'font_color': '#006100',
            'border': 1
        })
        total_format = workbook.add_format({
            'bold': True,
            'num_format': '#,##0.00',
            'border': 1
        })

        # Εγγραφή επικεφαλίδων στη γραμμή 0
        headers = ["ID", "Description", "Value", "Category", "Monthly", "Date"]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        # Ανάκτηση εξόδων, εσόδων και κατηγοριών από την εφαρμογή
        expenses = app.get_expenses_specific_month(month)["data"]
        print(expenses)
        incomes = app.get_incomes_specific_month(month)["data"]
        categories = {cat[0]: cat[1] for cat in app.categories}  # id -> name

        row = 1  # Ξεκινάμε από τη 2η γραμμή

        expenses_total = 0
        incomes_total = 0

        # Εγγραφή εξόδων
        if expenses:
            worksheet.merge_range(row, 0, row, 5, "EXPENSES", expense_header_format)
            row += 1

            for t in expenses:
                worksheet.write(row, 0, t[0])  # ID
                worksheet.write(row, 1, t[1])  # Περιγραφή
                worksheet.write(row, 2, t[2], currency_format)  # Ποσό
                worksheet.write(row, 3, categories.get(t[3], "Unknown"))  # Κατηγορία
                worksheet.write(row, 4, "Yes" if t[4] else "No")  # Μηνιαίο;
                worksheet.write(row, 5, t[5], date_format)  # Ημερομηνία
                row += 1

            # Σύνολο εξόδων
            expenses_total = sum(t[2] for t in expenses)
            worksheet.merge_range(row, 0, row, 3, "Total Expenses", total_format)
            worksheet.write(row, 4, expenses_total, total_format)
            row += 2  # Κενή γραμμή ανάμεσα στις ενότητες

        # Εγγραφή εσόδων
        if incomes:
            worksheet.merge_range(row, 0, row, 5, "INCOMES", income_header_format)
            row += 1

            for t in incomes:
                worksheet.write(row, 0, t[0])  # ID
                worksheet.write(row, 1, t[1])  # Περιγραφή
                worksheet.write(row, 2, t[2], currency_format)  # Ποσό
                worksheet.write(row, 3, categories.get(t[3], "Unknown"))  # Κατηγορία
                worksheet.write(row, 4, "Yes" if t[4] else "No")  # Μηνιαίο;
                worksheet.write(row, 5, t[5], date_format)  # Ημερομηνία
                row += 1

            # Σύνολο εσόδων
            incomes_total = sum(t[2] for t in incomes)
            worksheet.merge_range(row, 0, row, 3, "Total Incomes", total_format)
            worksheet.write(row, 4, incomes_total, total_format)
            row += 1

        # Καθαρή αποταμίευση (έσοδα - έξοδα)
        if expenses or incomes:
            net_savings = incomes_total - expenses_total
            net_format = workbook.add_format({
                'bold': True,
                'num_format': '#,##0.00',
                'bg_color': '#FFEB9C',
                'font_color': '#000000'
            })
            worksheet.merge_range(row, 0, row, 3, "NET SAVINGS", net_format)
            worksheet.write(row, 4, net_savings, net_format)

        # Ρύθμιση πλάτους στηλών
        worksheet.set_column('A:A', 10)   # ID
        worksheet.set_column('B:B', 25)   # Περιγραφή
        worksheet.set_column('C:C', 15)   # Ποσό
        worksheet.set_column('D:D', 20)   # Κατηγορία
        worksheet.set_column('E:E', 12)   # Μηνιαίο;
        worksheet.set_column('F:F', 12)   # Ημερομηνία

        # Κλείσιμο αρχείου και ειδοποίηση επιτυχίας
        workbook.close()
        messagebox.showinfo("Export Successful",
                            f"Exported {len(expenses)+len(incomes)} transactions to {filename}")

    # Αντιμετώπιση εξειδικευμένων ή γενικών σφαλμάτων
    except MainError as e:
        messagebox.showerror("error", str(e))
    except Exception as e:
        messagebox.showerror("error", f"Error exporting data: {str(e)}")

