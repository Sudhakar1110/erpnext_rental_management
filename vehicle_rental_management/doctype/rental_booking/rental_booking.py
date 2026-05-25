import frappe
from frappe.model.document import Document
from frappe.utils import date_diff, flt, get_datetime

class RentalBooking(Document):

    def validate(self):
        self.check_dates()
        self.check_vehicle_availability()
        self.compute_extra_amounts()
        self.compute_totals()

    def check_dates(self):
        if get_datetime(self.return_date) <= get_datetime(self.pickup_date):
            frappe.throw("Return date must be after pickup date")

    def check_vehicle_availability(self):
        clash = frappe.db.sql("""
            SELECT name FROM `tabRental Booking`
            WHERE vehicle = %s
              AND name != %s
              AND docstatus < 2
              AND status IN ('Confirmed','Checked Out','Reserved')
              AND NOT (return_date <= %s OR pickup_date >= %s)
        """, (self.vehicle, self.name or "", self.pickup_date, self.return_date))
        if clash:
            frappe.throw(f"Vehicle is already booked: {clash[0][0]}")

    def compute_extra_amounts(self):
        for row in (self.extras or []):
            rate = flt(row.rate) or frappe.db.get_value("Rental Extra", row.extra, "rate") or 0
            row.rate = rate
            charge_type = row.charge_type or frappe.db.get_value("Rental Extra", row.extra, "extra_type") or "Per Rental"
            qty = flt(row.quantity) or 1
            if charge_type == "Per Day":
                days = max(1, date_diff(self.return_date, self.pickup_date))
                row.amount = rate * qty * days
            else:
                row.amount = rate * qty

    def compute_totals(self):
        days = max(1, date_diff(self.return_date, self.pickup_date))
        self.rental_days = days
        if not self.daily_rate:
            self.daily_rate = frappe.db.get_value("Vehicle", self.vehicle, "daily_rate") or 0
        self.base_amount = flt(self.daily_rate) * days
        self.extras_total = sum(flt(e.amount) for e in (self.extras or []))
        subtotal = self.base_amount + self.extras_total - flt(self.discount_amount)
        tax_rate = frappe.db.get_single_value("Rental Settings", "default_tax_rate") or 0
        self.tax_amount = subtotal * flt(tax_rate) / 100
        self.grand_total = subtotal + self.tax_amount

    @frappe.whitelist()
    def get_tax_rate(self):
        return frappe.db.get_single_value("Rental Settings", "default_tax_rate") or 0


def validate_booking(doc, method):
    doc.validate()

def on_submit_booking(doc, method):
    frappe.db.set_value("Vehicle", doc.vehicle, "status", "Rented")
    doc.db_set("status", "Confirmed")
    email = frappe.db.get_value("Customer", doc.customer, "email_id")
    if email:
        frappe.sendmail(
            recipients=[email],
            subject=f"Booking Confirmed: {doc.name}",
            message=(
                f"Dear Customer,\n\n"
                f"Your booking {doc.name} has been confirmed.\n\n"
                f"Vehicle: {doc.vehicle}\n"
                f"Pickup: {doc.pickup_date} at {doc.pickup_location}\n"
                f"Return: {doc.return_date} at {doc.return_location}\n"
                f"Total: {doc.grand_total}\n\n"
                f"Thank you for choosing us."
            )
        )

def on_cancel_booking(doc, method):
    # Only release vehicle if no other active bookings
    other = frappe.db.exists("Rental Booking", {
        "vehicle": doc.vehicle,
        "name": ["!=", doc.name],
        "status": ["in", ["Confirmed", "Checked Out"]],
        "docstatus": ["<", 2]
    })
    if not other:
        frappe.db.set_value("Vehicle", doc.vehicle, "status", "Available")
    doc.db_set("status", "Cancelled")


@frappe.whitelist(allow_guest=True)
def create_web_booking(**kwargs):
    # Extract guest/user information
    email = kwargs.get("email")
    phone = kwargs.get("phone")
    cust_name = kwargs.get("customer_name")

    if frappe.session.user != "Guest":
        user_email = frappe.session.user
        customer = frappe.db.get_value("Customer", {"email_id": user_email}, "name")
        if not customer:
            user_fullname = frappe.db.get_value("User", user_email, "full_name") or user_email.split("@")[0]
            cust_doc = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": user_fullname,
                "customer_type": "Individual",
                "email_id": user_email
            })
            cust_doc.insert(ignore_permissions=True)
            customer = cust_doc.name
    else:
        if not email or not cust_name:
            frappe.throw("Customer Name and Email are required for booking.")
        
        customer = frappe.db.get_value("Customer", {"email_id": email}, "name")
        if not customer:
            cust_doc = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": cust_name,
                "customer_type": "Individual",
                "email_id": email,
                "mobile_no": phone
            })
            cust_doc.insert(ignore_permissions=True)
            customer = cust_doc.name

    # Validate mandatory inputs
    vehicle = kwargs.get("vehicle")
    if not vehicle:
        frappe.throw("Please select a vehicle.")

    pickup_date = kwargs.get("pickup_date")
    return_date = kwargs.get("return_date")
    if not pickup_date or not return_date:
        frappe.throw("Pickup and Return dates are required.")

    pickup_location = kwargs.get("pickup_location")
    return_location = kwargs.get("return_location")
    if not pickup_location or not return_location:
        frappe.throw("Pickup and Return locations are required.")

    # Process Extras checkboxes
    extras = []
    for key, val in kwargs.items():
        if key.startswith("extra_") and val:
            extras.append({
                "extra": val,
                "quantity": 1
            })

    # Create & Save Rental Booking
    booking = frappe.get_doc({
        "doctype": "Rental Booking",
        "customer": customer,
        "vehicle": vehicle,
        "pickup_date": pickup_date,
        "return_date": return_date,
        "pickup_location": pickup_location,
        "return_location": return_location,
        "special_requests": kwargs.get("special_requests"),
        "extras": extras,
        "status": "Draft",
        "source": "Website"
    })
    
    booking.insert(ignore_permissions=True)
    
    return {
        "status": "success",
        "message": "Booking created successfully!",
        "booking_name": booking.name
    }
