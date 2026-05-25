import frappe
from frappe.utils import today

def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Vehicle", "fieldname": "vehicle", "fieldtype": "Link", "options": "Vehicle", "width": 120},
        {"label": "License Plate", "fieldname": "license_plate", "fieldtype": "Data", "width": 130},
        {"label": "Type", "fieldname": "maintenance_type", "fieldtype": "Data", "width": 160},
        {"label": "Scheduled Date", "fieldname": "scheduled_date", "fieldtype": "Date", "width": 130},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 110},
        {"label": "Workshop", "fieldname": "workshop", "fieldtype": "Data", "width": 150},
        {"label": "Total Cost", "fieldname": "total_cost", "fieldtype": "Currency", "width": 130}
    ]

    conditions = "WHERE m.docstatus < 2"
    params = []

    if filters.get("from_date"):
        conditions += " AND m.scheduled_date >= %s"
        params.append(filters["from_date"])
    if filters.get("to_date"):
        conditions += " AND m.scheduled_date <= %s"
        params.append(filters["to_date"])
    if filters.get("status"):
        conditions += " AND m.status = %s"
        params.append(filters["status"])

    data = frappe.db.sql(f"""
        SELECT m.vehicle, v.license_plate, m.maintenance_type,
               m.scheduled_date, m.status, m.workshop, m.total_cost
        FROM `tabVehicle Maintenance` m
        LEFT JOIN `tabVehicle` v ON v.name = m.vehicle
        {conditions}
        ORDER BY m.scheduled_date ASC
    """, params, as_dict=True)

    return columns, data
