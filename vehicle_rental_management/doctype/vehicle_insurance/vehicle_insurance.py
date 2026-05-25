import frappe
from frappe.model.document import Document

class VehicleInsurance(Document):
    def on_submit(self):
        frappe.db.set_value("Vehicle", self.vehicle, "insurance_expiry", self.expiry_date)
        frappe.db.set_value("Vehicle", self.vehicle, "insurance_policy", self.policy_number)
