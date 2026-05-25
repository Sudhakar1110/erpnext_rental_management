import frappe

def after_install():
    create_roles()
    create_default_settings()
    frappe.db.commit()

def create_roles():
    for role in ["Fleet Manager", "Rental Agent", "Mechanic", "Driver"]:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1
            }).insert(ignore_permissions=True)

def create_default_settings():
    if not frappe.db.exists("Rental Settings", "Rental Settings"):
        doc = frappe.get_doc({
            "doctype": "Rental Settings",
            "default_tax_rate": 0,
            "default_currency": "USD",
            "late_return_fee_per_hour": 10,
            "terms_and_conditions": "Standard rental terms apply."
        })
        doc.insert(ignore_permissions=True)
