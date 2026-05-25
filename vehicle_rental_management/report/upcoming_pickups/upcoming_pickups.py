import frappe
from frappe.utils import add_days, today

def execute(filters=None):
    filters = filters or {}
    days = int(filters.get("days") or 7)
    to_date = add_days(today(), days)

    columns = [
        {"label": "Booking", "fieldname": "booking", "fieldtype": "Link", "options": "Rental Booking", "width": 140},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": "Pickup Date", "fieldname": "pickup_date", "fieldtype": "Datetime", "width": 160},
        {"label": "Return Date", "fieldname": "return_date", "fieldtype": "Datetime", "width": 160},
        {"label": "Location", "fieldname": "pickup_location", "fieldtype": "Link", "options": "Vehicle Location", "width": 130},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100}
    ]

    data = frappe.db.sql("""
        SELECT
            name AS booking, customer, vehicle,
            pickup_date, return_date, pickup_location,
            grand_total, status
        FROM `tabRental Booking`
        WHERE status = 'Confirmed'
          AND DATE(pickup_date) BETWEEN %s AND %s
          AND docstatus < 2
        ORDER BY pickup_date ASC
    """, (today(), to_date), as_dict=True)

    return columns, data
