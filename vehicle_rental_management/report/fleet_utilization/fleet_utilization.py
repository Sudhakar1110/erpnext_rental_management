import frappe
from frappe.utils import date_diff, getdate

def execute(filters=None):
    filters = filters or {}
    from_date = filters.get("from_date") or frappe.utils.add_months(frappe.utils.today(), -1)
    to_date = filters.get("to_date") or frappe.utils.today()
    period_days = max(1, date_diff(to_date, from_date) + 1)

    columns = [
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": "License Plate", "fieldname": "license_plate", "fieldtype": "Data", "width": 130},
        {"label": "Category", "fieldname": "category", "fieldtype": "Link", "options": "Vehicle Category", "width": 120},
        {"label": "Rented Days", "fieldname": "rented_days", "fieldtype": "Int", "width": 110},
        {"label": "Utilization %", "fieldname": "utilization", "fieldtype": "Percent", "width": 120},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 140},
        {"label": "No. of Bookings", "fieldname": "bookings", "fieldtype": "Int", "width": 130}
    ]

    veh_filters = {}
    if filters.get("category"):
        veh_filters["category"] = filters["category"]

    data = []
    for v in frappe.get_all("Vehicle", filters=veh_filters, fields=["name", "license_plate", "category"]):
        result = frappe.db.sql("""
            SELECT
                COALESCE(SUM(DATEDIFF(
                    LEAST(DATE(return_date), %s),
                    GREATEST(DATE(pickup_date), %s)
                ) + 1), 0) AS rented_days,
                COALESCE(SUM(grand_total), 0) AS revenue,
                COUNT(*) AS bookings
            FROM `tabRental Booking`
            WHERE vehicle = %s
              AND docstatus = 1
              AND status IN ('Checked Out','Checked In','Invoiced','Closed')
              AND DATE(pickup_date) <= %s
              AND DATE(return_date) >= %s
        """, (to_date, from_date, v.name, to_date, from_date), as_dict=True)

        rented_days = int(result[0].rented_days or 0) if result else 0
        data.append({
            "vehicle": v.name,
            "license_plate": v.license_plate,
            "category": v.category,
            "rented_days": rented_days,
            "utilization": round((rented_days / period_days) * 100, 2),
            "revenue": result[0].revenue if result else 0,
            "bookings": result[0].bookings if result else 0
        })

    data.sort(key=lambda x: x["utilization"], reverse=True)
    return columns, data
