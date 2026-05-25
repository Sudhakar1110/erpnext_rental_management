import frappe
from frappe import _
from frappe.model.document import Document
from rental_management.utils.calculations import (
    calculate_rental_days, calculate_rental_amount,
    calculate_discount, calculate_grand_total,
)

class RentalBooking(Document):
    def validate(self):
        self._validate_dates()
        self._check_vehicle_availability()
        self._calculate_totals()
        self._validate_license()

    def before_submit(self):
        if self.status not in ("Draft", "Confirmed"):
            frappe.throw(_("Only Draft or Confirmed bookings can be submitted."))
        self.status = "Confirmed"

    def on_submit(self):
        self._set_vehicle_status("Rented")

    def on_cancel(self):
        self.status = "Cancelled"
        self._set_vehicle_status("Available")

    def _validate_dates(self):
        if not self.start_date or not self.end_date:
            return
        if self.end_date <= self.start_date:
            frappe.throw(_("End Date must be after Start Date."))
        self.total_days = calculate_rental_days(self.start_date, self.end_date)

    def _check_vehicle_availability(self):
        if not self.vehicle or not self.start_date or not self.end_date:
            return
        vehicle_status = frappe.db.get_value("Rental Vehicle", self.vehicle, "status")
        if vehicle_status == "Maintenance":
            frappe.throw(_("Vehicle {0} is under maintenance.").format(self.vehicle))
        if vehicle_status == "Retired":
            frappe.throw(_("Vehicle {0} is retired.").format(self.vehicle))
        overlapping = frappe.db.sql("""
            SELECT name FROM `tabRental Booking`
            WHERE vehicle = %(vehicle)s AND name != %(name)s
              AND docstatus = 1 AND status IN ('Confirmed', 'Active')
              AND NOT (end_date <= %(start_date)s OR start_date >= %(end_date)s)
        """, {"vehicle": self.vehicle, "name": self.name,
               "start_date": self.start_date, "end_date": self.end_date})
        if overlapping:
            frappe.throw(_("Vehicle {0} is already booked. Conflict: {1}").format(
                self.vehicle, overlapping[0][0]))

    def _calculate_totals(self):
        if not self.total_days or not self.daily_rate:
            return
        self.rental_amount = calculate_rental_amount(self.total_days, self.daily_rate)
        self.discount_amount = calculate_discount(self.rental_amount, self.discount_percent or 0)
        self.grand_total = calculate_grand_total(self.rental_amount, self.discount_amount, self.damage_deposit or 0)

    def _validate_license(self):
        if self.license_expiry_date and self.end_date:
            expiry = frappe.utils.getdate(self.license_expiry_date)
            end = frappe.utils.getdate(self.end_date)
            if expiry < end:
                frappe.msgprint(_("Warning: Driver's license expires before rental end date."),
                                alert=True, indicator="orange")

    def _set_vehicle_status(self, status: str):
        frappe.db.set_value("Rental Vehicle", self.vehicle, "status", status)
        frappe.db.commit()

    @frappe.whitelist()
    def mark_active(self):
        if self.status != "Confirmed":
            frappe.throw(_("Only Confirmed bookings can be marked as Active."))
        self.status = "Active"
        self._set_vehicle_status("Rented")
        self.save()

    @frappe.whitelist()
    def complete_booking(self):
        if self.status != "Active":
            frappe.throw(_("Only Active bookings can be completed."))
        self.status = "Completed"
        self._set_vehicle_status("Available")
        self.save()
