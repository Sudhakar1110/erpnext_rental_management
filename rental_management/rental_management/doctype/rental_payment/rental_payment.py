import frappe
from frappe import _
from frappe.model.document import Document

class RentalPayment(Document):
    def validate(self):
        self._validate_amount()
        self._validate_booking()

    def before_submit(self):
        self.status = "Received"

    def on_cancel(self):
        self.status = "Refunded"

    def _validate_amount(self):
        if self.amount <= 0:
            frappe.throw(_("Payment amount must be greater than zero."))

    def _validate_booking(self):
        if not self.booking:
            return
        booking = frappe.get_doc("Rental Booking", self.booking)
        if booking.status == "Cancelled":
            frappe.throw(_("Cannot add payment to a Cancelled booking."))
        if not self.customer:
            self.customer = booking.customer
