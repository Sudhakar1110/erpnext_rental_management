import frappe

def execute(filters=None):
    filters = filters or {}
    from_date = filters.get("from_date") or frappe.utils.add_months(frappe.utils.today(), -1)
    to_date = filters.get("to_date") or frappe.utils.today()

    columns = [
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": "License Plate", "fieldname": "license_plate", "fieldtype": "Data", "width": 130},
        {"label": "Make / Model", "fieldname": "make_model", "fieldtype": "Data", "width": 160},
        {"label": "Category", "fieldname": "category", "fieldtype": "Data", "width": 120},
        {"label": "Bookings", "fieldname": "bookings", "fieldtype": "Int", "width": 100},
        {"label": "Total Days", "fieldname": "total_days", "fieldtype": "Int", "width": 100},
        {"label": "Base Revenue", "fieldname": "base_revenue", "fieldtype": "Currency", "width": 140},
        {"label": "Extras Revenue", "fieldname": "extras_revenue", "fieldtype": "Currency", "width": 140},
        {"label": "Total Revenue", "fieldname": "total_revenue", "fieldtype": "Currency", "width": 140}
    ]

    data = frappe.db.sql("""
        SELECT
            rb.vehicle,
            v.license_plate,
            CONCAT(v.make, ' ', v.model) AS make_model,
            v.category,
            COUNT(rb.name) AS bookings,
            SUM(rb.rental_days) AS total_days,
            SUM(rb.base_amount) AS base_revenue,
            SUM(rb.extras_total) AS extras_revenue,
            SUM(rb.grand_total) AS total_revenue
        FROM `tabRental Booking` rb
        LEFT JOIN `tabVehicle` v ON v.name = rb.vehicle
        WHERE rb.docstatus = 1
          AND rb.status IN ('Checked In','Invoiced','Closed')
          AND DATE(rb.pickup_date) BETWEEN %s AND %s
        GROUP BY rb.vehicle
        ORDER BY total_revenue DESC
    """, (from_date, to_date), as_dict=True)

    return columns, data
