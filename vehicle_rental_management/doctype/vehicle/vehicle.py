import frappe
from frappe.model.document import Document

class Vehicle(Document):
    def validate(self):
        if self.year and (self.year < 1950 or self.year > 2100):
            frappe.throw("Invalid Year")
        if self.odometer and self.odometer < 0:
            frappe.throw("Odometer cannot be negative")
        if self.daily_rate and self.daily_rate < 0:
            frappe.throw("Daily rate cannot be negative")

    def set_status(self, status):
        self.db_set("status", status)

    def on_update(self):
        # Check if any date fields are expiring soon and create alerts
        from frappe.utils import add_days, today, getdate
        threshold = add_days(today(), 30)
        for field, label in [
            ("insurance_expiry", "Insurance"),
            ("registration_expiry", "Registration"),
            ("roadworthiness_expiry", "Roadworthiness"),
            ("next_service_date", "Service"),
        ]:
            val = self.get(field)
            if val and getdate(val) <= getdate(threshold):
                frappe.msgprint(
                    f"Warning: {label} for {self.license_plate} is due on {val}",
                    alert=True,
                    indicator="orange"
                )


@frappe.whitelist()
def get_available_vehicles(from_date, to_date, category=None, location=None):
    """Return vehicles not booked in the given date range."""
    filters = {"status": "Available"}
    if category:
        filters["category"] = category
    if location:
        filters["current_location"] = location

    vehicles = frappe.get_all(
        "Vehicle",
        filters=filters,
        fields=["name", "license_plate", "make", "model", "category",
                "daily_rate", "weekly_rate", "image", "seats", "transmission", "fuel_type"]
    )

    booked = frappe.db.sql("""
        SELECT vehicle FROM `tabRental Booking`
        WHERE docstatus < 2
          AND status IN ('Confirmed','Checked Out','Reserved')
          AND NOT (return_date <= %s OR pickup_date >= %s)
    """, (from_date, to_date), as_list=True)
    booked_set = {b[0] for b in booked}
    return [v for v in vehicles if v["name"] not in booked_set]
