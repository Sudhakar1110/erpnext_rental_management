import frappe
from frappe.model.document import Document

class RentalAgreement(Document):
    def validate(self):
        if not self.terms_and_conditions:
            self.terms_and_conditions = frappe.db.get_single_value(
                "Rental Settings", "terms_and_conditions"
            ) or ""

    def on_submit(self):
        self.db_set("status", "Active")
        create_sales_invoice(self, None)
        # Link back to booking
        frappe.db.set_value("Rental Booking", self.booking, "agreement", self.name)


def create_sales_invoice(doc, method):
    if doc.sales_invoice:
        return
    booking = frappe.get_doc("Rental Booking", doc.booking)
    si = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": doc.customer,
        "due_date": frappe.utils.today(),
        "items": [{
            "item_code": frappe.db.get_single_value("Rental Settings", "rental_item_code") or "RENTAL-SERVICE",
            "description": f"Vehicle Rental: {doc.vehicle} ({booking.rental_days} days)",
            "qty": 1,
            "rate": booking.grand_total
        }]
    })
    si.insert(ignore_permissions=True)
    doc.db_set("sales_invoice", si.name)
