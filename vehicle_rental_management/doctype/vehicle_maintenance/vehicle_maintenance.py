import frappe
from frappe.model.document import Document
from frappe.utils import flt

class VehicleMaintenance(Document):
    def validate(self):
        self.total_cost = flt(self.labour_cost) + flt(self.parts_cost)

    def on_submit(self):
        if self.status == "Completed":
            updates = {}
            if self.next_service_date:
                updates["next_service_date"] = self.next_service_date
            if self.next_service_km:
                updates["next_service_km"] = self.next_service_km
            if self.odometer_at_service:
                updates["odometer"] = self.odometer_at_service
            if updates:
                frappe.db.set_value("Vehicle", self.vehicle, updates)
            frappe.db.set_value("Vehicle", self.vehicle, "status", "Available")

    def before_submit(self):
        if self.status not in ("Completed", "Cancelled"):
            frappe.throw("Please mark maintenance as Completed or Cancelled before submitting")
        # Set vehicle to Maintenance when in progress
        if self.status == "In Progress":
            frappe.db.set_value("Vehicle", self.vehicle, "status", "Maintenance")
