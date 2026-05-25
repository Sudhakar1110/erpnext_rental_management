import frappe
from frappe.model.document import Document
from frappe.utils import flt

class FuelLog(Document):
    def validate(self):
        self.total_cost = flt(self.litres) * flt(self.cost_per_litre)
        if self.odometer:
            frappe.db.set_value("Vehicle", self.vehicle, "odometer", self.odometer)
