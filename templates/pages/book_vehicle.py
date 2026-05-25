import frappe

def get_context(context):
    vehicle_name = frappe.form_dict.get("vehicle")
    if vehicle_name:
        context.vehicle = frappe.get_doc("Vehicle", vehicle_name)
    else:
        context.vehicle = None
        
    context.extras = frappe.get_all(
        "Rental Extra",
        filters={"is_active": 1},
        fields=["name", "extra_name", "extra_type", "rate", "description"]
    )
    
    context.locations = frappe.get_all(
        "Vehicle Location",
        filters={"is_active": 1},
        fields=["name", "location_name", "city"]
    )
    
    # Pre-populate logged-in user or customer profile info
    context.user_logged_in = frappe.session.user != "Guest"
    if context.user_logged_in:
        context.user_email = frappe.session.user
        cust = frappe.get_all("Customer", filters={"email_id": frappe.session.user}, fields=["customer_name", "mobile_no"], limit=1)
        if cust:
            context.customer_name = cust[0].customer_name
            context.customer_phone = cust[0].mobile_no or ""
        else:
            context.customer_name = frappe.db.get_value("User", frappe.session.user, "full_name") or frappe.session.user.split("@")[0]
            context.customer_phone = ""
    else:
        context.user_email = ""
        context.customer_name = ""
        context.customer_phone = ""

    context.no_cache = 1
    return context
