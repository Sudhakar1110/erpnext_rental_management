import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, add_days

class Driver(Document):
    def validate(self):
        if self.license_expiry and getdate(self.license_expiry) < getdate(today()):
            frappe.msgprint(
                f"Warning: Driver {self.full_name} license has expired on {self.license_expiry}",
                alert=True,
                indicator="red"
            )
        elif self.license_expiry and getdate(self.license_expiry) <= getdate(add_days(today(), 30)):
            frappe.msgprint(
                f"Warning: Driver {self.full_name} license expires on {self.license_expiry}",
                alert=True,
                indicator="orange"
            )
