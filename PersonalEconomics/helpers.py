from datetime import datetime


def format_date(date):
    if isinstance(date, datetime):
        return date.strftime("%Y-%m-%d")
    elif isinstance(date, str):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
            try:
                date_obj = datetime.strptime(date, fmt)
                return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError(f"Μη έγκυρη μορφή ημερομηνίας: {date}")



def success_response(data):
    return {"success": True, "data": data}


def error_response(errors):
    return {"success": False, "errors": errors if isinstance(errors, list) else [errors]}

from monthly_expenses_chart import create_chart1
from yearly_chart import create_chart2
from monthly_incomes_chart import create_chart3

def refresh_chart1(app):
    if app.chart_widget1:
        app.chart_widget1.destroy()
    app.chart_widget1 = create_chart1(app.chart_frame, app)
    app.chart_widget1.grid(sticky="nsew")

def refresh_chart2(app):
    if hasattr(app, "chart_widget2") and app.chart_widget2:
        app.chart_widget2.destroy()
    if hasattr(app, "chart_frame2"):
        app.chart_widget2 = create_chart2(app.chart_frame2, app)
        app.chart_widget2.grid(sticky="nsew")

def refresh_chart3(app):
    if hasattr(app, "chart_widget3") and app.chart_widget3:
        app.chart_widget3.destroy()
    if hasattr(app, "chart_frame3"):
        app.chart_widget3 = create_chart3(app.chart_frame3, app)
        app.chart_widget3.grid(sticky="nsew")

def refresh_all_charts(app):
    refresh_chart1(app)
    refresh_chart2(app)
    refresh_chart3(app)
