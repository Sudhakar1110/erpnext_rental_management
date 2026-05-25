import frappe
from frappe.utils import add_days, today, now_datetime

def send_pickup_reminders():
    """Send email reminders 24h before pickup."""
    tomorrow = add_days(today(), 1)
    bookings = frappe.get_all(
        "Rental Booking",
        filters={
            "status": "Confirmed",
            "pickup_date": ["between", [tomorrow + " 00:00:00", tomorrow + " 23:59:59"]]
        },
        fields=["name", "customer", "vehicle", "pickup_date", "pickup_location"]
    )
    for b in bookings:
        email = frappe.db.get_value("Customer", b.customer, "email_id")
        if email:
            frappe.sendmail(
                recipients=[email],
                subject=f"Pickup Reminder: {b.name}",
                message=(
                    f"Dear Customer,\n\n"
                    f"This is a reminder that you are picking up vehicle {b.vehicle} "
                    f"tomorrow ({tomorrow}) at {b.pickup_location}.\n\n"
                    f"Booking Reference: {b.name}\n\n"
                    f"Thank you for choosing us."
                )
            )

def check_overdue_returns():
    """Flag and notify on overdue returns."""
    overdue = frappe.get_all(
        "Rental Booking",
        filters={"status": "Checked Out", "return_date": ["<", now_datetime()]},
        fields=["name", "customer", "vehicle", "return_date"]
    )
    for b in overdue:
        # Notify fleet managers
        managers = frappe.get_all("Has Role", filters={"role": "Fleet Manager"}, fields=["parent"])
        for m in managers:
            frappe.sendmail(
                recipients=[m.parent],
                subject=f"OVERDUE RETURN: {b.name}",
                message=(
                    f"Booking {b.name} for vehicle {b.vehicle} is overdue.\n"
                    f"Expected return: {b.return_date}\nCustomer: {b.customer}"
                )
            )
        # Notify customer
        email = frappe.db.get_value("Customer", b.customer, "email_id")
        if email:
            frappe.sendmail(
                recipients=[email],
                subject=f"Action Required: Overdue Return - {b.name}",
                message=(
                    f"Your rental of vehicle {b.vehicle} was due on {b.return_date}. "
                    f"Please return the vehicle immediately to avoid additional charges."
                )
            )

def check_document_expiry():
    """Check insurance and registration expiry."""
    threshold = add_days(today(), 30)
    # Insurance expiry
    for v in frappe.get_all(
        "Vehicle",
        filters={"insurance_expiry": ["<=", threshold], "status": ["!=", "Out of Service"]},
        fields=["name", "license_plate", "insurance_expiry"]
    ):
        managers = frappe.get_all("Has Role", filters={"role": "Fleet Manager"}, fields=["parent"])
        for m in managers:
            frappe.sendmail(
                recipients=[m.parent],
                subject=f"Insurance Expiry Warning: {v.license_plate}",
                message=f"Vehicle {v.license_plate} insurance expires on {v.insurance_expiry}."
            )
    # Registration expiry
    for v in frappe.get_all(
        "Vehicle",
        filters={"registration_expiry": ["<=", threshold]},
        fields=["name", "license_plate", "registration_expiry"]
    ):
        managers = frappe.get_all("Has Role", filters={"role": "Fleet Manager"}, fields=["parent"])
        for m in managers:
            frappe.sendmail(
                recipients=[m.parent],
                subject=f"Registration Expiry Warning: {v.license_plate}",
                message=f"Vehicle {v.license_plate} registration expires on {v.registration_expiry}."
            )

def check_maintenance_due():
    """Create ToDo tasks for vehicles due for maintenance."""
    for v in frappe.get_all(
        "Vehicle",
        filters={"next_service_date": ["<=", today()]},
        fields=["name", "license_plate", "next_service_date"]
    ):
        # Check if ToDo already exists
        existing = frappe.db.exists("ToDo", {
            "reference_type": "Vehicle",
            "reference_name": v.name,
            "status": "Open"
        })
        if not existing:
            frappe.get_doc({
                "doctype": "ToDo",
                "description": f"Service due for {v.license_plate} (due: {v.next_service_date})",
                "reference_type": "Vehicle",
                "reference_name": v.name,
                "priority": "High"
            }).insert(ignore_permissions=True)

def sync_telematics():
    """Placeholder: poll telematics provider API and create Telematics Log entries."""
    # Implement provider-specific API calls here
    # Example: Geotab, Samsara, Webfleet, etc.
    pass
