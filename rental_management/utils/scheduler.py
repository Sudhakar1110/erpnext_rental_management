import frappe
from frappe import _

def mark_overdue_bookings():
    today = frappe.utils.today()
    overdue = frappe.db.get_all(
        "Rental Booking",
        filters={"status": "Active", "end_date": ["<", today], "docstatus": 1},
        fields=["name", "customer", "customer_name", "vehicle", "end_date"],
    )
    for booking in overdue:
        frappe.get_doc({
            "doctype": "ToDo",
            "description": _("Overdue Rental: Booking {name} for {customer_name} on vehicle {vehicle} was due {end_date}.").format(**booking),
            "reference_type": "Rental Booking",
            "reference_name": booking.name,
            "priority": "High",
            "status": "Open",
        }).insert(ignore_permissions=True)
    if overdue:
        frappe.db.commit()
