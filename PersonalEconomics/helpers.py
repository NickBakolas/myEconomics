from datetime import datetime


def format_date(date):
    if isinstance(date, datetime):
        return date.strftime("%d-%m-%Y")
    elif isinstance(date, str):
        try:
            # Αν έρχεται από tkcalendar
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            return date_obj.strftime("%d-%m-%Y")
        except ValueError:
            try:
                date_obj = datetime.strptime(date, "%d-%m-%Y")
                return date_obj.strftime("%d-%m-%Y")
            except ValueError as e:
                raise ValueError(f"Μη έγκυρη μορφή ημερομηνίας: {date}") from e
    else:
        raise TypeError(
            "Η ημερομηνία πρέπει να είναι string ή αντικείμενο datetime.")



def success_response(data):
    return {"success": True, "data": data}


def error_response(errors):
    return {"success": False, "errors": errors if isinstance(errors, list) else [errors]}

from expenses_chart import create_chart1
from month_chart import create_chart2
from incomes_chart import create_chart3


def refresh_chart1(app):
    if hasattr(app, "chart_widget1") and app.chart_widget1:
        app.chart_widget1.destroy()

    if hasattr(app, "chart_frame1"):
        app.chart_widget1 = create_chart1(app.chart_frame1, app)
        app.chart_widget1.grid(row=0, column=0, sticky="nsew")



def refresh_chart2(app):
    if hasattr(app, "chart_widget2") and app.chart_widget2:
        app.chart_widget2.destroy()

    if hasattr(app, "chart_frame2"):
        app.chart_widget2 = create_chart2(app.chart_frame2, app)
        app.chart_widget2.grid(row=0, column=0, sticky="nsew")


def refresh_chart3(app):
    if hasattr(app, "chart_widget3") and app.chart_widget3:
        app.chart_widget3.destroy()

    if hasattr(app, "chart_frame3"):
        app.chart_widget3 = create_chart3(app.chart_frame3, app)
        app.chart_widget3.grid(row=0, column=0, sticky="nsew")


def refresh_all_charts(app):
    refresh_chart1(app)
    refresh_chart2(app)
    refresh_chart3(app)
