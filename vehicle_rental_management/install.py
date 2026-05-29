import frappe
from frappe import _

def after_install():
    create_roles()
    create_workflow()
    create_default_settings()
    create_custom_fields()
    frappe.db.commit()

def after_migrate():
    """Run after each migrate to ensure any new fixtures are applied."""
    create_roles()
    create_workflow()
    create_default_settings()
    create_custom_fields()
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

def create_workflow():
    """Create the Rental Booking Workflow if it doesn't exist."""
    if not frappe.db.exists("Workflow", "Rental Booking Workflow"):
        workflow = frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Rental Booking Workflow",
            "document_type": "Rental Booking",
            "is_active": 1,
            "workflow_state_field": "status",
            "states": [
                {"state": "Draft", "doc_status": "0", "allow_edit": "Rental Agent"},
                {"state": "Confirmed", "doc_status": "1", "allow_edit": "Rental Agent"},
                {"state": "Checked Out", "doc_status": "1", "allow_edit": "Rental Agent"},
                {"state": "Checked In", "doc_status": "1", "allow_edit": "Rental Agent"},
                {"state": "Invoiced", "doc_status": "1", "allow_edit": "Fleet Manager"},
                {"state": "Closed", "doc_status": "1", "allow_edit": "Fleet Manager"},
                {"state": "Cancelled", "doc_status": "2", "allow_edit": "Fleet Manager"},
            ],
            "transitions": [
                {"state": "Draft", "action": "Confirm", "next_state": "Confirmed", "allowed": "Rental Agent", "allow_self_approval": 1},
                {"state": "Confirmed", "action": "Check Out", "next_state": "Checked Out", "allowed": "Rental Agent", "allow_self_approval": 1},
                {"state": "Checked Out", "action": "Check In", "next_state": "Checked In", "allowed": "Rental Agent", "allow_self_approval": 1},
                {"state": "Checked In", "action": "Invoice", "next_state": "Invoiced", "allowed": "Fleet Manager", "allow_self_approval": 1},
                {"state": "Invoiced", "action": "Close", "next_state": "Closed", "allowed": "Fleet Manager", "allow_self_approval": 1},
                {"state": "Confirmed", "action": "Cancel", "next_state": "Cancelled", "allowed": "Fleet Manager", "allow_self_approval": 1},
                {"state": "Draft", "action": "Cancel", "next_state": "Cancelled", "allowed": "Fleet Manager", "allow_self_approval": 1},
            ],
        })
        workflow.insert(ignore_permissions=True)
        frappe.msgprint(_("Rental Booking Workflow created successfully"))

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
