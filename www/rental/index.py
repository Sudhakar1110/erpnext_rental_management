import frappe

def get_context(context):
    settings = frappe.get_single("Rental Settings")
    context.portal_title = settings.portal_title or "Rent a Vehicle"
    context.categories = frappe.get_all("Vehicle Category", fields=["name", "category_name", "image"])
    context.vehicles = frappe.get_all(
        "Vehicle",
        filters={"status": "Available"},
        fields=["name", "license_plate", "make", "model", "year",
                "daily_rate", "image", "category", "seats", "transmission", "fuel_type"],
        order_by="category asc, daily_rate asc",
        limit=48
    )
    context.no_cache = 1
    return context
