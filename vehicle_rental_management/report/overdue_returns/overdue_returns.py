import frappe
from frappe.utils import now_datetime, time_diff_in_hours

def execute(filters=None):
    columns = [
        {"label": "Booking", "fieldname": "booking", "fieldtype": "Link", "options": "Rental Booking", "width": 140},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": "Expected Return", "fieldname": "return_date", "fieldtype": "Datetime", "width": 160},
        {"label": "Hours Overdue", "fieldname": "hours_overdue", "fieldtype": "Float", "width": 120},
        {"label": "Daily Rate", "fieldname": "daily_rate", "fieldtype": "Currency", "width": 120},
        {"label": "Est. Late Fee", "fieldname": "late_fee", "fieldtype": "Currency", "width": 130},
        {"label": "Customer Phone", "fieldname": "phone", "fieldtype": "Data", "width": 130}
    ]

    overdue = frappe.db.sql("""
        SELECT
            rb.name AS booking,
            rb.customer,
            rb.vehicle,
            rb.return_date,
            rb.daily_rate,
            c.mobile_no AS phone
        FROM `tabRental Booking` rb
        LEFT JOIN `tabCustomer` c ON c.name = rb.customer
        WHERE rb.status = 'Checked Out'
          AND rb.return_date < %s
          AND rb.docstatus < 2
        ORDER BY rb.return_date ASC
    """, (now_datetime(),), as_dict=True)

    late_fee_rate = frappe.db.get_single_value("Rental Settings", "late_return_fee_per_hour") or 0
    data = []
    for row in overdue:
        hours = round(time_diff_in_hours(now_datetime(), row.return_date), 1)
        row.hours_overdue = hours
        row.late_fee = hours * float(late_fee_rate)
        data.append(row)

    return columns, data
