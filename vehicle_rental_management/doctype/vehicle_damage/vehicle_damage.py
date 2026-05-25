import frappe
from frappe.model.document import Document

class VehicleDamage(Document):
    def on_submit(self):
        if self.severity == "Total Loss":
            frappe.db.set_value("Vehicle", self.vehicle, "status", "Out of Service")
