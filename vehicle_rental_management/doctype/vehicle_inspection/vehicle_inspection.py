import frappe
from frappe.model.document import Document

class VehicleInspection(Document):
    def on_submit(self):
        if self.odometer_reading and self.vehicle:
            frappe.db.set_value("Vehicle", self.vehicle, "odometer", self.odometer_reading)
