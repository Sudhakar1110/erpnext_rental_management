import frappe

@frappe.whitelist()
def get_bookings():
    return {'status': 'success'}