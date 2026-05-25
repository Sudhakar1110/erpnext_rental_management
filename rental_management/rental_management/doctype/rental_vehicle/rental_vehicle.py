import frappe
from frappe.model.document import Document

class RentalVehicle(Document):
    def validate(self):
        self._validate_rates()
        self._validate_year()

    def _validate_rates(self):
        if self.daily_rate <= 0:
            frappe.throw("Daily Rate must be greater than zero.")
        if self.weekly_rate and self.weekly_rate < self.daily_rate:
            frappe.msgprint("Weekly Rate is less than Daily Rate. Please confirm.", alert=True)
        if self.monthly_rate and self.monthly_rate < self.weekly_rate:
            frappe.msgprint("Monthly Rate is less than Weekly Rate. Please confirm.", alert=True)

    def _validate_year(self):
        import datetime
        current_year = datetime.date.today().year
        if self.year and (self.year < 1980 or self.year > current_year + 1):
            frappe.throw(f"Year must be between 1980 and {current_year + 1}.")

    def on_update(self):
        if self.status == "Available":
            pass

    @frappe.whitelist()
    def get_effective_rate(self, days: int) -> float:
        days = int(days)
        if days >= 28 and self.monthly_rate:
            return float(self.monthly_rate) * (days / 30)
        elif days >= 7 and self.weekly_rate:
            weeks = days // 7
            remaining = days % 7
            return float(self.weekly_rate) * weeks + float(self.daily_rate) * remaining
        return float(self.daily_rate) * days
