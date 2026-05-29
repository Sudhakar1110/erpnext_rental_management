import frappe
from frappe import _

def after_install():
    create_roles()
    create_default_settings()
    create_custom_fields()
    frappe.db.commit()

def after_migrate():
    """Run after each migrate to ensure any new fixtures are applied."""
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

def create_custom_fields():
    """Create custom fields on standard ERPNext DocTypes as needed."""
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    custom_fields = {
        "Customer": [
            {
                "fieldname": "rental_customer_section",
                "label": _("Rental Management"),
                "fieldtype": "Section Break",
                "insert_after": "territory"
            },
            {
                "fieldname": "driving_license_no",
                "label": _("Driving License No"),
                "fieldtype": "Data",
                "insert_after": "rental_customer_section"
            },
            {
                "fieldname": "license_expiry_date",
                "label": _("License Expiry Date"),
                "fieldtype": "Date",
                "insert_after": "driving_license_no"
            }
        ]
    }
    create_custom_fields(custom_fields)
